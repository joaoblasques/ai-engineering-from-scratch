# Exercise 1 — Branch Workflow

> **Lived example:** this lesson was built on `feature/phase-00-lesson-02`, which
> *is* the exercise — clone, branch, commit, push — in production form. The steps
> below trace exactly what was done, so you can follow the same pattern for your
> own `my-progress` branch.

## What the exercise asks

> Clone this repo, create a branch called `my-progress`, make a file, commit it, push it.

## Constraint for this course build

Per the project convention the `my-progress` branch is not duplicated in this
repo — `feature/phase-00-lesson-02` serves as the canonical lived example of the
same workflow.

## Walkthrough (mirror these steps for your own fork)

```bash
# 1. Clone (if not already cloned)
git clone https://github.com/rohitg00/ai-engineering-from-scratch.git
cd ai-engineering-from-scratch

# 2. Create and switch to your branch
git checkout -b my-progress
# (this repo used: git checkout -b feature/phase-00-lesson-02)

# 3. Make a file
echo "hello git" > hello.txt

# 4. Stage and commit
git add hello.txt
git commit -m "feat: add hello.txt — my first commit"

# 5. Push to your fork
git push origin my-progress
```

## What actually happened on this branch

```bash
git checkout -b feature/phase-00-lesson-02   # step 2
# ... created lesson deliverables ...
git add -A                                    # step 4
git commit -m "feat(00-02): ..."
git push origin feature/phase-00-lesson-02   # step 5
```

The mechanism is identical. The only difference is branch name and content.

## Key concept

A branch is a **pointer** to a commit. `git checkout -b` creates the pointer and
moves HEAD to it. Every subsequent commit advances the pointer. Nothing on `main`
changes until you explicitly merge.
