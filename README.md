# cns_project

1. Install firefox version 66. I have uploaded zip for the same. <br/>
2. Install geckodriver. <br/>
   1.1 Download the zip and extract it. <br/>
   1.2 chmod +x geckodriver <br/>
   1.3 sudo mv -f geckodriver /usr/local/share/geckodriver <br/>
   1.4 sudo ln -s /usr/local/share/geckodriver /usr/local/bin/geckodriver <br/>
   1.5 sudo ln -s /usr/local/share/geckodriver /usr/bin/geckodriver <br/>

3. Clone the repo : https://github.com/Himanshu-g81/cns_project.git <br/>
4. Install requirement file using : python3.7 -m pip install -r requirements.txt <br/>
5. You will not be able to use face authentication because code contains logic for detecting my face only. <br/>
6. For executing the bot directly, move to him_bot directory and execute bot using : python3.7 main.py <br/>


<h2> NOTE </h2>
   Kindly do not install firefox with root privilages. For doing that kindly make another user (wihtout sudo previlages) than install firefox there otherwise geckodriver will give runtime error. And try to perform attack as the secondary user <br/>
 
 Video tutorial of attack: https://www.youtube.com/watch?v=dwRFxYgTGsk
 Tested on ubuntu 18.04
 For any issue or query kindly contact: hgwalani81@gmail.com

