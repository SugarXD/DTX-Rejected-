#Script will push the app to the remote server
#Requires user interaction

echo "Please enter the necessary information as needed."

#OS detection
os=${OSTYPE//[0-9.]/}

if [[ "$os" == 'darwin' ]] #Mac
	then
	/usr/local/bin/px login
	/usr/local/bin/px push
else #Windows
	echo "Please input instructions for pushing to Predix from Windows in push_remote.sh"
fi

