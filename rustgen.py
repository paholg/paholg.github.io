#!/usr/bin/env python3

# Simple script to make rustdoc --test and Jekyll coexist nicely

import subprocess, glob, sys, os


# Take my special markdown files and turn them into what Jekyll wants.
def fix_md(source, target):
    in_code = False
    with open(target, "w") as targ, open(source, "r") as src:
        for l in src:
            if "```" in l:
                in_code = not in_code
            if in_code:
                l = l.replace("```ignore", "```rust")
                l = l.replace("```continue", "```rust")
                if l.lstrip().startswith("# "):
                    l = ""
            targ.write(l)

def gen_test_chunks(source, target):
    in_code = False
    in_main = False
    in_prelude = False

    snippets = []
    main = ""
    prelude = ""

    with open(source, "r") as src:
        for l in src:
            if "```rust" in l:
                in_code = True
                snippets.append(l)
            elif "```prelude" in l:
                in_prelude = True
            elif "```main" in l:
                in_main = True
            elif "```\n" in l:
                if in_code:
                    snippets[-1] += l
                    in_code = False
                elif in_prelude:
                    in_prelude = False
                elif in_main:
                    in_main = False
            elif in_prelude:
                prelude += l
            elif in_main:
                main += l
            elif in_code:
                snippets[-1] += l

    with open(target, "w") as targ:
        targ.write("```rust\n" + prelude + "\nfn main() {\n" + main + "}\n```")
        for s in snippets:
            targ.write(s)

# def fix_ex(source, target):
#     in_top = True
#     with open(target, "w") as targ, open(source, "r") as src:
#         for l in src:
#             if in_top:
#                 if "/*" in l:
#                     l = ""
#                 elif "*/" in l:
#                     l = "\n```rust\n"
#                     in_top = False
#             targ.write(l)
#         targ.write("\n```\n")

result = subprocess.call(["cargo", "update"], cwd="gen/")
if result != 0:
    exit(result)
result = subprocess.call(["cargo", "build"], cwd="gen/")
if result != 0:
    exit(result)

extern = ""
for dep in glob.glob("gen/target/debug/deps/lib*.?lib"):
    begin = dep.index("lib")
    end = dep.index("-")
    name = dep[begin+3:end]
    extern += " --extern {}={}".format(name, dep)

dirs = glob.glob("gen/_*/")

for d in dirs:
    files = glob.glob(d + "*.md")
    for f in files:
        gen_test_chunks(f, "gen/temp.md")
        print("Testing: {}".format(f))
        test = "rustdoc --test gen/temp.md" + extern + " -L dependency=gen/target/debug/deps" + " -L dependency=gen/target/debug"
        print(test)
        result = subprocess.call(test, shell=True)
        if result != 0:
            exit(result)
        fix_md(f, f[4:])
    # examples = glob.glob(d + "examples/*.rs")
    # for ex in examples:
    #     fix_ex(ex, ex[4:-3]+".md")
