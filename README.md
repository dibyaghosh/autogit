# AutoGit

Python library for creating periodic git backups of your codebase (e.g. right before launching an experiment).

```python
import autogit
autogit.backup('path_to_my_repo')
```

This code-snippet will save an exact copy of your code to a side branch (e.g. `main-backup` if the current branch is `main`) with a timestamp-marked commit.

**Why might this be useful?**

When I run an experiment, it can be really useful to preserve exactly what the codebase looked like when I ran the experiment, in case I want to post-analyze later. Oftentime this is useful for really small or potentially temporary changes that I either don't want to be permanent, or isn't worth making a full real commit for.

**What does it look like?**

I've actually been using autogit while writing this library! Check out the [main-backup](https://github.com/dibyaghosh/autogit/tree/main-backup) branch on this repo.

## Installation

This package requires you to have `git` installed on your machine, but nothing else really. Also Python 3.6+. Install it like any of your other python libraries.


```
 pip install git+https://github.com/dibyaghosh/autogit.git
```
