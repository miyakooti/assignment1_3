
 # LoadModule wsgi_module /home/ubuntu/.local/lib/python3.10/site-packages


 # vim: syntax=apache ts=4 sw=4 sts=4 sr noet
 <VirtualHost *:80>
     ServerName ec2-54-172-191-147.compute-1.amazonaws.com:80
     DocumentRoot /home/ubuntu/assignment2
     WSGIScriptAlias / /home/ubuntu/assignment2/adapter.wsgi

     <Directory "/home/ubuntu/assignment2/">
         Options +Indexes +FollowSymLinks +ExecCGI
         Require all granted
     </Directory>
 </VirtualHost>
