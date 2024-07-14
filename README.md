# HackBot

1. Install firefox version 66 or later.<br/>
2. Install geckodriver. <br/>
   1.1 Download the zip and extract it. <br/>
   1.2 chmod +x geckodriver <br/>
   1.3 sudo mv -f geckodriver /usr/local/share/geckodriver <br/>
   1.4 sudo ln -s /usr/local/share/geckodriver /usr/local/bin/geckodriver <br/>
   1.5 sudo ln -s /usr/local/share/geckodriver /usr/bin/geckodriver <br/>

3. Clone the repo : https://github.com/Himanshu-g81/cns_project.git <br/>
4. Install all requirements: python3.7 -m pip install -r requirement.txt <br/>
5. You need to do some more work for using face detection else you could directly move to step 6. <br/>
   5.1 Install cv2 library of python3 <br/>
   5.2 execute faceDataCollection.py in him_bot directory using : python3 faceDataCollection.py <br/>
   5.3 It will ask you for name and collect your face data. <br/>
   5.4 To make your face as authenticator, in bot_begin file at line 120, 136 change name 'himanshu' -> 'your name' <br/>
   5.5 execute bot_begin using command : python3 bot_begin.py <br/>
6. For executing the bot directly, move to him_bot directory and execute bot using : python3.7 main.py <br/>


<h2> NOTE </h2>
   Kindly do not install firefox with root privilages. For doing that kindly make another user (wihtout sudo previlages) than install firefox there otherwise geckodriver will give runtime error. And try to perform attack as the secondary user <br/>
 <br/>
 Video tutorial of attack: https://www.youtube.com/watch?v=dwRFxYgTGsk <br/>
 Tested on ubuntu 18.04 <br/>
 For any issue or query kindly contact: hgwalani81@gmail.com

