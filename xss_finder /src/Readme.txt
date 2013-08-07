Hey Everyone,

I am releasing my script to check XSS (Cross Site Scripting) in any given Url.
Its a simple script with event driven menu where you can test all your GET and POST urls.
I wrote the whole code in python but to make it simple for everyone to run it I wrote a small shell script which you just need to run  (follow instruction) and it will take care of everything from taking inputs to testing. I tried minimum human intervention .
You just run the script go have a cup of coffee and it will do the rest of work and will inform you if it finds anything suspicious.
The reason I started  with XSS  is because its most common vulnerability in our website as well as in all other websites as well.

How to use the script:

1) Unzip the attached file  and change your current working directory to the folder you have unzipped in command prompt.
2) Please read the "How_to" file for making config changes.
3) In command prompt type "sh xss.sh"
4) It will take you through a event driven menu to get the URL you want to test
5) Then it will start testing the given URL ( It can take upto 1 - 5 minutes depending upon the no. of parameters and payload )
6) If any of the parameter in URL is vulnerable then you will see it in command prompt else you will see "Nothing Found " message .

Some dependencies/configuration:
1)xss.cfg file contains basic configuration please make required changes there before running the script.

Hope this will make your life easier and will add extra layer of security ,so that everything can be tested with this first before being pushed to prod.

Note:I would be releasing its web version soon with many changes.

#Contact info:"m.shadab.sidd@gmail.com"


