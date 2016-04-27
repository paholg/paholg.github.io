#!/usr/bin/env python3

# Simple script to make rustdoc --test and Jekyll coexist nicely
# Special syntax:
# #---FNAME.md
# JEKYLL HEADER STUFF
# ---#
# begins a test file, named FNAME.md
#
# ```rust
# ```
# is a normal, self-contained code block
#
# ```prelude
# ```
# goes into the continuous code block, before main()
#
# ```main
# ```
# goes into the continuous code block, inside main()

import subprocess, glob, sys, os


# Take my special markdown files and turn them into what Jekyll wants.
def fix_md(source, target):
    in_code = False
    in_header = False
    with open(target, "w") as targ, open(source, "r") as src:
        for l in src:
            if "#---" in l:
                in_header = True
            elif "---#" in l:
                in_header = False
            elif not in_header:
                if "```" in l:
                    in_code = not in_code
                if in_code:
                    l = l.replace("```ignore", "```rust")
                    l = l.replace("```prelude", "```rust")
                    l = l.replace("```main", "```rust")
                    if l.lstrip().startswith("# "):
                        l = ""
                targ.write(l)

def gen_test_chunks(source, target_dir):
    in_file = False
    in_header = False
    in_code = False
    in_main = False
    in_prelude = False

    snippets = []
    main = ""
    prelude = ""

    header = ""
    fname = ""

    def save_test(f, header, fname, main, prelude, snippets):
        print("Creating and testing: {}".format(f))
        with open(f, "w") as target:
            target.write(header + "\n" + "```rust\n" + prelude + "\nfn main() {\n" + main + "}\n```")
            for s in snippets:
                target.write(s)
        test = "rustdoc --test " + f + extern + " -L dependency=gen/target/debug/deps" + " -L dependency=gen/target/debug"
        print(test)
        result = subprocess.call(test, shell=True)
        if result != 0:
            exit(result)

    with open(source, "r") as src:
        for l in src:
            if not in_file and "```" in l:
                print("Found code block without knowing file information to put it in.")
                exit(1)

            if l[0:2] == "# ":
                l = l[2:]
            if "#---" in l:
                if in_file:
                    f = target_dir + "examples/" + fname
                    save_test(f, header, fname, main, prelude, snippets)
                    header = ""
                    fname = ""
                    main = ""
                    prelude = ""
                    snippets = []
                in_file = True
                in_header = True
                header += "---\n"
                fname = l[4:-1]
            elif "---#" in l:
                in_header = False
                header += "---\n"
            elif in_header:
                header += l

            if "```rust" in l:
                in_code = True
                snippets.append("\n" + l)
            elif "```prelude" in l:
                prelude += "\n"
                in_prelude = True
            elif "```main" in l:
                main += "\n"
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
                main += "    " + l
            elif in_code:
                snippets[-1] += l
        f = target_dir + "examples/" + fname
        save_test(f, header, fname, main, prelude, snippets)


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
        print("Mucking with: {}".format(f))
        gen_test_chunks(f, d[4:])
        fix_md(f, f[4:])
    # examples = glob.glob(d + "examples/*.rs")
    # for ex in examples:
    #     fix_ex(ex, ex[4:-3]+".md")

result = subprocess.call(["jekyll", "b"])
if result != 0:
    exit(result)
