tmp=`sudo grep -e '( \t)PermitRootLogin( \t)no' /etc/ssh/sshd_config`
ret=$?
echo $tmp
echo $?
sudo grep -e '( \t)PermitRootLogin( \t)no' /etc/ssh/sshd_config
if [ $ret ]
then
	echo 'OK'
else
	echo `sudo grep  PermitRootLogin /etc/ssh/sshd_config`
fi
