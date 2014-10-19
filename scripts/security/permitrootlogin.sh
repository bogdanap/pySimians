tmp=`sudo grep -e '( \t)PermitRootLogin( \t)no' /etc/ssh/sshd_config`
if [ $? ]
then
	echo 'OK'
else
	echo `sudo grep -e PermitRootLogin /etc/ssh/sshd_config`
fi
