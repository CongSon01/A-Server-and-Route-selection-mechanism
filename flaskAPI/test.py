import subprocess
for i in range(1,10000):
    if (i==5):
        subprocess.call('python api/app.py','-e', shell=True)
    print(i)