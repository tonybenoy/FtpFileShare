cd /home/pi/FtpFileShare
source venv/bin/activate
python /home/pi/FtpFileShare/pyftpserver.py -p "Tony" -u "Tony" -H "127.0.0.1" -f "/media/pi" -rwdcg <<EOF
y
EOF
