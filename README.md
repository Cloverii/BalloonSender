## BalloonSender

BalloonSender is a script which can crawl new ACs and display them on the screen during a contest on [CQUOJ](http://acm.cqu.edu.cn/). Having given out a balloon to the team solving the problem, you can mark the record as "Done", so that it won't be shown again.

### Requirement
Python 2.7

### Download
- Clone or download this repository.

### Running
- If you are a  Windows user, you may need a text editor which supports Unix new line character, for example, *notepad++*.
- Open the file `conf.json`, you can edit the contest id and colors of balloons for  different problems.
- Open the shell (or cmd), change working directory to where `BalloonSender.py` locates. Enter `python BalloonSender.py`.
- To stop the BalloonSender, enter `Ctrl + C` in shell (or cmd).
- You need to refresh manually.

### Some points
- Duplication won't be shown. That means when a team gets more than one AC for a problem, only the first AC record will be shown on the screen.
- Records are shown out of order.

### Todo List
- [x] Improve UI
- [ ] Add GUI configuration
- [ ] Try not to crawl all ACs every time
- [ ] Refresh automatically
- [ ] Add support to the location of teams

### Support
If you need help, contact [cloveriiw@gmail.com](mailto:cloveriiw@gmail.com).

### Change Log
v0.1.0.
- First release

v0.2.0.
- Remove duplicate records
- Improve UI

v0.2.1.
- Add README
- Format the config file

v0.2.2

- Fix README

v0.3.0

- Add support to private contests
- Display hints when contest is unavailable

v0.3.1

- Fix the bug that all contests are shown as unavailable
- Improve UI (fix the window and format the text)

v0.3.2

- Fix the bug that crashing when colors of balloons are not correctly set
- Improve the display of records