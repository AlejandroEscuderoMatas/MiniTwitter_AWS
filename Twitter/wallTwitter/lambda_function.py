import sys
import logging
import pymysql
import json
import base64
from urllib.parse import parse_qs

rds_host = "3.230.84.50"

username = "admin"
password ="password"
dbname = "twitter"


def lambda_handler(event , context):
    print(json.dumps(event));
    
    email="err";
    password="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded :
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            email=decodedEvent["email"][0];
            password=decodedEvent["password"][0];
    else:
        email=event["body"]["email"];
        password=event["body"]["password"];
        
    print(email);
    print(password);
    
  
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("select * from users where email='"+email+"' and password = '"+password+"'");
            
            loginToken = cur.fetchone();
            
            if(loginToken)
                return {
                    'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'OK' , 'user': loginToken[0] , 'password': loginToken[1]} )
                }
                
            else
                return {
                    'statusCode': 400,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'notOK' , 'msg': 'User not exists' )
                }
            
            conn.commit();
            cur.close();
    except pymysql.MySQLError as e:    
        print (e)
    conn.close();
    
