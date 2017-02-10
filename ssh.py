#-*- coding: utf-8 -*-
#!/usr/bin/python 
import paramiko
import threading

# 登陆SSH2方法
def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=1)
        
        transport = paramiko.Transport((ip,22))
        transport.connect(username=username,password=passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('F:/work/nsfocus/yidong/tool/base-line/v1.0/base-line.sh','/tmp/base-line.sh')
        #sftp.put('F:/work/nsfocus/yidong/tool/base-line/v1.0/run-base-line.sh','/tmp/run-base-line.sh')
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
#           stdin.write("Y")   #简单交互，输入 ‘Y’ 
            out = stdout.readlines()
            #屏幕输出
            for o in out:
                print o,
        print '%s\tOK\n'%(ip)
        ssh.close()
    except Exception, e:
        print e
        print '%s\tError\n'%(ip)

if __name__=='__main__':
    #cmd = ['echo ' + base_line_str + '>>/tmp/bsl.sh', cat  ,base_line_str]#你要执行的命令列表
    #cmd = ['echo "' + base_line_str + '"' + '>>/tmp/bsl.sh', 'cat /tmp/bsl.sh']#你要执行的命令列表
    #print 'echo "' + base_line_str + '"' + '>>/tmp/bsl.sh'
    # 登陆后输入的命令
    cmd = ['chmod 755 /tmp/base-line.sh']
    username = "root"  #用户名
    passwd = "000000"    #密码
    threads = []   #多线程
    print "Begin......"
    
    f = open("ip.txt", "r")  
    done = 0
    while not done:
        ip = str(f.readline()).strip()
        if ip:
            if(ip == '#'):
                done = 1
            ssh2(ip,username,passwd,cmd)
    f.close()
    
    #ssh2('10.48.226.1',username,passwd,cmd)
    # for i in range(67,69):
    #     #ssh2('10.48.226.1',username,passwd,cmd)
    #     ssh2('10.46.115.'+str(i),username,passwd,cmd)
    #     #threading.Thread(target=ssh2,args=('10.48.226.'+str(i),username,passwd,cmd)).start()