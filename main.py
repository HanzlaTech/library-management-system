from fastapi import FastAPI, HTTPException, status, Request,Response,Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import connection
import pymysql
from jose import jwt
from fastapi import Header    
from fastapi import FastAPI, HTTPException 
from datetime import datetime,timedelta
from pwdlib import PasswordHash
from fastapi import Depends  
from fastapi.responses import JSONResponse
from email_validator import validate_email,EmailNotValidError
import secrets
import smtplib
from logger import log
from email.message import EmailMessage
from fastapi import UploadFile,File,Form
import os   
from PIL import Image
from io import BytesIO 
import uuid
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler
from exceptions import(handler403,handler429,handler422,handler503,handler500)
from slowapi.errors import RateLimitExceeded
from customclass import InternalServer_Error
from fastapi.staticfiles import StaticFiles

limiter=Limiter(key_func=get_remote_address)
from dotenv import load_dotenv
import os
     # huzaifa new code 
globalUser_id=None   
Secret_Key=os.environ["JWT_secret"]
Algorithm="HS256"
password_hash=PasswordHash.recommended()
Refresh_Secret_key="refresh" 
app=FastAPI()

app.state.Limiter=limiter
@app.middleware("http")
async def middleware(request:Request,call_next):
    log.info("---------------------------")
    log.info("middleware for that endpoint: %s runs" ,request.url.path)
    log.info("cookies : %s",request.cookies)
    public_path=["/signup","/login","/refresh","/logout","/email","/upload","/docs","/redoc","/openapi.json"]
    if request.url.path in public_path:
        return await call_next(request)
    access=request.cookies.get("access")
    if access is not None:
     try:
        data=jwt.decode(
            access,
            Secret_Key,
            algorithms=[Algorithm]
        )
        request.state.user={
            "role":data["role"],
            "userid":data["userid"],
            "picture":data["URL"]
        } 
        response=await call_next(request)
        return response          
     except Exception:
      return JSONResponse(
        status_code=401,
        content={"msg": "access_token_expired",'status':False}
    )
    else:
         return JSONResponse(
                status_code=401,
                content={"msg": "cookies is expired"}
            )    
def userrole(request:Request):
    user=request.state.user
    if(user["role"]=="User"):
       return True
    else :
        return False

def adminrole(request:Request):
    user=request.state.user
    if user["role"]=="Admin":
        return True
    elif user["role"]=="User":
        return False





             # Exception handling

app.add_exception_handler(
    ConnectionError,
    handler503
)

app.add_exception_handler(
     TimeoutError ,
    handler503
)

app.add_exception_handler(
    RateLimitExceeded,
    handler429
)

app.add_exception_handler(
    HTTPException,
    handler403
)

app.add_exception_handler(
    InternalServer_Error,
    handler500
)


app.add_exception_handler(
    RequestValidationError,
    handler422
)







app.add_middleware(
    CORSMiddleware,
   allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ], # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class LoginSchema (BaseModel):
    email:str
    password:str
class Request_Schema(BaseModel):
   ID:int
class Accept_Schema(BaseModel):
   
    Bookid:int
    userid:int
class Return_Schema(BaseModel):
    ISBN:int
    userid:int
class SigninSchema (BaseModel):
    email:str
    password:str
class cancel_Schema(BaseModel):
    id:int
class Reject_Schema(BaseModel):
    Bookid:int
    userid:int
class User_record_Schema(BaseModel):
    userid:int
class OTP_Schema(BaseModel):
    OTP:int
    Userid:int   
    
@app.get("/refresh")
def refresh(response:Response,refresh:str=Cookie(None)):
    log.info("requst for refrsh api recieved")
    try:
        
        data=jwt.decode(
            refresh,
            Refresh_Secret_key,
            algorithms=[Algorithm]
        )
        log.info("data extract from  refresh token ")
        payload={
        "userid":data["userid"],
        "role":data["role"],
        "email":data["email"],
        "URL":data['URL'],
        "exp":datetime.utcnow()+timedelta(minutes=10)
    }
        log.info("refresh-payload is create")
        token=jwt.encode(
        payload,
        Secret_Key,
        algorithm=Algorithm
    )
        log.info("access token is create")
        refresh_payload={
            "userid":data["userid"],
            "role":data["role"],
            "email":data["email"],
            "URL":data['URL'],
            "exp":datetime.utcnow()+timedelta(days=7)
        }
        log.info("refresh payload is create")
        refresh=jwt.encode(
            refresh_payload,
            Refresh_Secret_key,
            algorithm=Algorithm
        )
        log.info("refresh token is create")
        response.set_cookie(
            key="access",
            value=token,
            httponly=True,
            path="/",
            secure=False,
            samesite="lax",
            max_age=10*60
            
        )
        log.info("access token is create in cookies")
        response.set_cookie(
            key="refresh",
            value=refresh,
            path="/refresh",
            httponly=True,
            samesite="strict",
            secure=False,
            max_age=7*24*60*60
        )
        log.info("refresh token is create in cookies")
    except Exception:
        log.info("error occur in token creation")
        raise HTTPException(
            status_code=500,
            detail="error in creating token code"
        )
    
       


@app.post("/signup")
async def signup(email:str=Form(),password:str=Form(),file:UploadFile=File()): 


  log.info("request recieved for upload file api")
  filename=""  
  data=await file.read()
  log.info("data is read from file")
  if data is not None:
         log.info("file is not empty")
         if file.filename is not None:
          extension=os.path.splitext(file.filename)[1]
          log.info("extract extension from file")
          if len(data)>=5*1024*1024 :
                          log.info("our file is more than 5mb")
                          raise HTTPException(
                              status_code=400,
                              detail="File size is greater than 5 MB"
                          ) 
          elif extension.lower() not in [".jpg",".png",".webp",".pdf",".jpeg"]:
                                  log.info("our file extension is wrong")
                                  raise HTTPException(
                                      status_code=400,
                                      detail="Extension dont match"
          
                                  )
      
          elif file.content_type not in ["image/jpg","image/png","image/jpeg","image/webp"]:
              log.info("this file is not a image")
              raise HTTPException(
                  status_code=400,
                  detail="this is not a image please send a correct info"
              )
          elif True:
                try:
                    image=Image.open(BytesIO(data))
                    image.verify()
                except Exception:
                    log.info(" Invalid image")
                    raise HTTPException(
                        status_code=400,
                        detail="picture is not image"
                    )
                try:
                    image=Image.open(BytesIO(data))
                    width,height=image.size
                    if width >5000 or height>5000:
                        raise Exception       
                except:
                    log.info("pic with greater dimensions are upload")
                    raise HTTPException(
                       status_code=400,
                      detail="please upload less size picture"
                 ) 
          filename=str(uuid.uuid4())+extension          
          fil=open("D:pic/"+filename,"wb")
          fil.write(data)
          fil.close()    
            
         
  else:
                    raise HTTPException(
                     status_code=400,
                         detail="No file is send"
                     )        
    



  log.info('signup First log is here')
  hashed_password=password_hash.hash(password)  
  log.info("password is hash")
  connection.ping(reconnect=True)
  cursor=connection.cursor(pymysql.cursors.DictCursor)
 
  try:
   result=validate_email(email)
   log.info("emial format is correct")
   cursor.execute("Insert into users(Email,Password,Role,Email_Verified,URL) values(%s,%s,%s,%s,%s)",
                    (email,hashed_password,"User",False,filename))   
   
   
   cursor.execute("Select * from users where Email=%s",(email))
   user=cursor.fetchone()
   
   otp=secrets.randbelow(1000000)
   otp=f"{otp:06d}"
   sender="hafeezhanzla24@gmail.com"
   password="otec jkeu wvkh lfor"
   reciever=email
   msg=EmailMessage()
   msg["Subject"]="Email Verfication OTP"
   msg["From"]=sender
   msg["To"]=reciever
   msg.set_content(f"Your OTP is :{otp}")
   with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
         server.login(sender,password)
         server.send_message(msg)  
   log.info("otp is send")      
   if user is not None:
    cursor.execute("Insert into OTP(OTP,User_id) values(%s,%s)",(otp,user["User_id"],))
    connection.commit()
    log.info("insert otp in otp table or changing in database are save")
    cursor.close()
    # app.mount("/uploads",StaticFiles(directory="upload"),name="uploads")
    app.mount("/pic",StaticFiles(directory="D:/pic"),name="uploads")
    
    return {
        "Userid":user["User_id"]
    }
  except pymysql.err.IntegrityError:
      log.error("email exist already")
      raise HTTPException(
          status_code=409,
          detail="Email exist already"
      )
 

  except Exception as e:   
    return JSONResponse(
        status_code=500,
        content={'msg':'Error occur %s'%type(e).__name__,'status':False}
    )

     
@app.post("/email")
def email(data:OTP_Schema):
 try:
    log.info("request recieved for otp verify")
    connection.ping(reconnect=True)
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("Select * from OTP where User_id=%s",(data.Userid,))
    log.info("database query execute")
    user=cursor.fetchone()
   
    if user is not None:
        log.info("DB OTP: %s, type: %s", user["OTP"], type(user["OTP"]).__name__)
        log.info("Request OTP: %s, type: %s", data.OTP, type(data.OTP).__name__)
        if user["OTP"]==data.OTP:
           
            cursor.execute("update users set Email_Verified=%s where User_id=%s",(True,data.Userid,))
            log.info("otp is verified")
            connection.commit()
        else:
            log.info("invalid otp")
            raise HTTPException(
                status_code=401,
                detail="Invalid OTP"
            )
    else: 
        log.exception("for that user_id no user exist")
        raise HTTPException(
            status_code=402,
            detail="user is None"
        )
 except pymysql.err.ProgrammingError:
      return JSONResponse(
          status_code=500,
          content={'msg':'mysql query dont execute','status':False}
      )
 except Exception:
      raise InternalServer_Error("Internal Server Error",500)     
        

@app.post("/login")
@limiter.limit("5/minute")
def login(data:LoginSchema,response:Response,request:Request):
   try: 
    log.info("Request arrives in log endpoint")
    log.info("Request data")
    log.info(data)
    log.info(request)
    connection.ping(reconnect=True)
    log.info("Database connect occur")
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("Select * from users where Email=%s AND Email_Verified=%s",(data.email,True))
    log.info("Database query execute")
    user=cursor.fetchone()
    cursor.close()
    if user is not None:
     log.info("User exist in database")
     if password_hash.verify(data.password,user["Password"]):
        log.info("password is hash")
        payload={
            "userid":user["User_id"],
            "role":user["Role"],
            "email":user["Email"],
            
            "URL":user["URL"],
            "exp":datetime.utcnow()+timedelta(minutes=1)
        }
        log.info("payload for access token is create")
        token=jwt.encode(
            payload,
            Secret_Key,
            algorithm=Algorithm
        )
        log.info("access token is create")
        refresh_payload={
            "userid":user["User_id"],
            "role":user["Role"],
            "email":user["Email"],
            "URL":user["URL"],
            "type":"refresh",
            "exp":datetime.utcnow()+timedelta(days=7)
        }
        log.info("refresh payload is create")
        refresh=jwt.encode(
            refresh_payload,
            Refresh_Secret_key,
            algorithm=Algorithm
        )
        log.info("refresh token is create")
        
        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7*24*60*60,
            path="/refresh"
           
        )
        log.info("access cookie is create")
        response.set_cookie(
            key="access",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=10*60,
            path="/"
           
        )
        log.info("refresh cookie is create")
        log.info("user data : %s",user)
        return {
            "status":200,
            "detail":{'msg':'Login Successfull','status':True,'role':user["Role"]}
        }
            
            
        
     else:
        raise InternalServer_Error("Incorrect password",500)
         
     
    else :
      log.info("User with that info dont exist")
      raise HTTPException(
            status_code=400,
            detail = f"User with {data.email} doesn't exist"
        )
   except pymysql.err.ProgrammingError:
         return JSONResponse(
             status_code=500,
             content={'msg':'mysql query dont execute','status':False}
         )
     
        
   
        




    
# borrow request
@app.post("/request")
def borrow_request(req: Request_Schema,request:Request,user=Depends(userrole)):
 try:
  log.info("Request for book borrow is recieved")
  if user:
       log.debug("Correct Role mean user called borrow books api")
       dat=request.state.user
       log.info("take data from request.state.user and store dat")
       cursor=connection.cursor(pymysql.cursors.DictCursor)
       log.info("database connection occur")
       cursor.execute("Select * from books where Book_id=%s",(req.ID,))
       log.info("execute query: Select * from books where Book_id=%s,(req.ID,) ")
       row=cursor.fetchone()
       log.info("take row from cursor obj")
       if row is not None:
                        log.info("confirm that cursor row is not empty mean book exist for that book id")
                        cursor.execute("""insert into record(User_id,Book_id,Status) 
                                values (%s,%s,%s)""",(dat["userid"],row["Book_id"],"Requested",))
       else:
                  raise HTTPException(
                      status_code=400,
                      detail="This book-id dont exist"
                  )
       log.info("insert book in record table")
       connection.commit()
       log.info("save changes in database")

       cursor.close()
       log.info("close the cursor")
       return "your request is send"
       
  else :
     log.exception("admin cannot call borrow books api")
     raise HTTPException(
         status_code=403,
         detail="Admin cannot do that"
     )
 except pymysql.err.ProgrammingError:
      return JSONResponse(
          status_code=500,
          content={'msg':'mysql query dont execute','status':False}
      )
 except Exception:
      raise InternalServer_Error("Internal Server Error",500)  
# request response
@app.post("/accept")
def request_respons(req: Accept_Schema,user=Depends(adminrole)):
 try:
    log.debug("request for accept book is acheived")
    if user:   
        log.info("admin is called that api")
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        log.info("database connection occur")
        cursor.execute("""Update record
                      set Status=%s
                      where (User_id=%s and Book_id=%s)""",("Borrowed",req.userid,req.Bookid))
        log.info("database query execute")
        connection.commit()
        log.info("database changes is saved")
        cursor.close()
        log.info("close the cursor")
    else:
        log.error("user cannot called that accept book api")
        raise HTTPException(
            status_code=403,
            detail="User cannot do that"
        ) 

 except pymysql.err.ProgrammingError:
       return JSONResponse(
           status_code=500,
           content={'msg':'mysql query dont execute','status':False}
       )
 except Exception:
       raise InternalServer_Error("Internal Server Error",500)    
@app.post("/reject")
def request_response(req: Reject_Schema,user=Depends(adminrole)):
 try:
  log.info("requst recieved for reject books ")
  if user:
            log.info("admin send request for reject api")
            connection.ping(reconnect=True)  
            log.info("database connection occur")
            cursor=connection.cursor(pymysql.cursors.DictCursor)
            log.info("Cursor object is made")
            cursor.execute("Delete from record where(User_id=%s and Book_id=%s)",(req.userid,req.Bookid))
            log.info("database query execute")
            connection.commit()
            log.debug("Database changes saved")
           
            
  else :
      log.exception("user cannot reject that")
      raise HTTPException(
          status_code=403,
          detail="User cannot do that"
      )
 except pymysql.err.ProgrammingError:
       return JSONResponse(
           status_code=500,
           content={'msg':'mysql query dont execute','status':False}
       )
 except Exception:
       raise InternalServer_Error("Internal Server Error",500)  

@app.post("/cancel_request")
def cancel(data:cancel_Schema,request:Request,user=Depends(userrole)):
 log.info("request recieved at cancel request")
 try:
    if user:
        log.info("correct role like user call cancel request api")
        dat=request.state.user  
        connection.ping(reconnect=True)
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Delete from record where (User_id=%s and Book_id=%s)",(dat["userid"],data.id,))
        log.info("query execute for cancel request")
        connection.commit()
        log.info("changes save in connection")

        return "Request is canceled"
    else:
        log.exception("admin dont called that cancel api")
        raise HTTPException(
            status_code=403,
            detail="Admin cannot do that"
         )
 except pymysql.err.ProgrammingError:
     return JSONResponse(
         status_code=500,
         content={'msg':'mysql query dont execute','status':False}
     )
 except Exception:
     raise InternalServer_Error("Internal Server Error",500)  

@app.get("/admin")
def show_all_books_admin(user=Depends(adminrole)):
 try:
  if user:
        log.info("request receved for to show all book")
        connection.ping(reconnect=True)  
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select * from books where books.Book_id not in (Select Book_id from record)")
        log.info("query execute for freebooks")
        admin=cursor.fetchall()
        cursor.execute("Select b.Book_id,b.Book_name,b.Book_isbn,b.Author_name,r.Status from record r inner join books b on r.Book_id =b.Book_id where r.Status=%s",("Borrowed",))
        log.info("query execute for borowboooks")
        admin2=cursor.fetchall()
        return {
            "list1":admin,
            "list2":admin2
        }
  else:
     log.error("user cannot call that showbooks api")
     raise HTTPException(
         status_code=403,
         detail="User cannot do that"
     )
 except pymysql.err.ProgrammingError:
     return JSONResponse(
         status_code=500,
         content={'msg':'mysql query dont execute','status':False}
     )
 except Exception:
     raise InternalServer_Error("Internal Server Error",500)  
    
@app.get("/requested_books")
def requested_books(user=Depends(adminrole)):
 try:
    log.info("request recieved for requested books")
    if user:
        log.info("correct role :admin , call that api ")
        connection.ping(reconnect=True)
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select r.User_id,r.Book_id,b.Book_isbn,b.Book_name,b.Author_name from record r join books b on r.Book_id=b.Book_id where r.Status=%s",("Requested",))
        log.info("database query execute")
        request=cursor.fetchall()

        if request is not None:
         return request
    else:
        log.error("user cannot call that api")
        raise HTTPException(
            status_code=403,
            detail="User cannot do that"
            
        )
 except pymysql.err.ProgrammingError:
         return JSONResponse(
             status_code=500,
             content={'msg':'mysql query dont execute','status':False}
         )
 except Exception:
         raise InternalServer_Error("Internal Server Error",500)  
@app.get("/freebooks")
def show_all_books(user=Depends(userrole)):
 try:
    log.info("request recieved for freebooks api")
    if user:
        log.info("correct role:user, call that api")
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select * from books where Book_id not in (Select Book_id from record)")
        log.info("database query execute")
        free=cursor.fetchall()
        cursor.close()
        return free
    else:
        log.exception("admin cannot call that api")
        raise HTTPException(
            status_code=403,
            detail='Admin cannot do that'
        )
 except pymysql.err.ProgrammingError:
      return JSONResponse(
          status_code=500,
          content={'msg':'mysql query dont execute','status':False}
      )
 except Exception:
      raise InternalServer_Error("Internal Server Error",500)     
@app.get("/userrecord",)  
def user_record(request:Request,user=Depends(userrole)):
 try:
    log.info("request recieved for userrecord api")
    if user:   
         log.info("correct role:user, call userrecord api")
         dat=request.state.user         
         cursor=connection.cursor(pymysql.cursors.DictCursor)
         cursor.execute("Select b.Book_id,b.Book_name,b.Book_isbn,b.Author_name ,r.Status from record r inner join books b on r.Book_id=b.Book_id where r.User_id=%s",(dat["userid"],))
         log.info("database query execute")
         books=cursor.fetchall()
         cursor.close()
         return books
    else:
        log.info("admin call that userrecord api")
        raise HTTPException(
            status_code=403,
            detail="Admin cannot do that"
        )   
 except pymysql.err.ProgrammingError:
      return JSONResponse(
          status_code=500,
          content={'msg':'mysql query dont execute','status':False}
      )
 except Exception:
      raise InternalServer_Error("Internal Server Error",500)     
   

@app.get("/auth/check")
def auth(request:Request):
    log.info("request recieved for auth/check")
    data=request.state.user
    return JSONResponse(
        status_code=200,
        content={'detail':'token is valid','status':True,"role":data["role"]}
    )
    
    log.info("return 200 status")

@app.get("/picture")
def picture(request:Request):
 data=request.state.user
 return data["picture"]

@app.post("/logout")
def logout(response:Response):
    log.info("request recieved for logout api")
    response.delete_cookie(
        key="access",
        path="/"
        
    )
    response.delete_cookie(
        key="refresh",
        path="/refresh"
    )
    log.info("both access or refresh token are deleted")
    raise InternalServer_Error("Internal Server Error",500)


