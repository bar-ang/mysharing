import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("bar.ang16@gmail.com", "crt123569")
 
msg = "Ahoy there!"
server.sendmail("bar.ang16@gmail.com", "bar.ang16@gmail.com", msg)
server.quit()