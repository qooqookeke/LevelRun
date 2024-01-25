from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import EmailNotValidError, validate_email
from utils import check_password, hash_password

# 회원가입
class UserRegisterResource(Resource) :
    def post(self) :
        data = request.get_json()        

        # 이메일 유효성 검사
        try :
            validate_email(data['email'])

        except EmailNotValidError as e :
            print(e)
            return {"Error" : str(e)}, 400

        # 비밀번호 길이 검사
        if len(data['password']) < 4 and len(data['password']) > 14 :
            return {"Error" : "비밀번호 길이가 올바르지 않습니다."}, 400

        # 단방향 암호화된 비밀번호를 저장
        password = hash_password(data['password'])

        try :
            connection = get_connection()

            query = '''insert into user
                    (nickName, email, password, type)
                    value(%s, %s, %s, 0);'''
            record = (data['nickName'], data['email'], password)

            cursor = connection.cursor()
            cursor.execute(query, record)

            # 회원가입시 생성한 유저아이디를 데이터베이스에서 가져와
            # 초기 레벨 테이블 정보를 넣어준다.
            userId = cursor.lastrowid

            query = '''insert into level
                        (userId)
                        values
                        (%s);'''

            record = (userId,)
            
            # 커서 초기화 
            cursor = connection.cursor()
            cursor.execute(query, record)

            # exercise 테이블 생성
            query = '''insert into exercise
                        (userId)
                        values
                        (%s);'''

            record = (userId,)

            cursor = connection.cursor()
            cursor.execute(query, record)            

            # randomBox 테이블 생성
            query = '''insert into randomBox
                        (userId)
                        values
                        (%s);'''

            record = (userId,)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"Error" : str(e)}, 500
        
        # user 테이블의 id로 JWT 토큰을 만들어야 한다.
        access_token = create_access_token(userId)
        
        return {"result" : "success", "accessToken" : access_token}, 200


    pass

# 로그인
class UserLoginResource(Resource) :
    def post(self) :
        data = request.get_json()
        try :
            connection = get_connection()

            query = '''select id, nickName, email, password 
                        from user
                        where email = %s;'''
            
            record = (data['email'],)

            # 딕셔너리 형태로 가져옴
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500        

        # 가입정보 확인
        if len(result_list) == 0 :
            return {"Error" : "회원가입된 정보가 없습니다."}, 400
                
        password = str(data['password'])
        

        check = check_password(password, result_list[0]['password'])
        if check == False :
            return {"error" : "비밀번호가 맞지 않습니다."}, 406
        
        # 암호화 토큰생성
        access_token = create_access_token(result_list[0]['id'])

        return {"result" : "success", "accessToken" : access_token}, 200
    

# 카카오 가입 닉네임 중복 체크
class KakaoLoginResource(Resource) :
    def post(self) :
        data = request.get_json()
        nickName = data["nickName"]
        email = data["email"]        
        profileUrl = data['profileUrl']
        type = data['type']

        try :
            connection = get_connection()

            query = '''select id, nickName, email, password
                    from user
                    where email = %s;'''
            
            record = (email,)

            # 딕셔너리 형태로 가져옴
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            # 이메일 정보가 있을 때
            if len(result_list) != 0 :
                if result_list[0]['password'] != 'kakao' :
                    cursor.close()
                    connection.close()
                    return {"result" : "해당 이메일 주소로 가입된 정보가 있습니다."}, 400
            
                # 카카오 유저 데이터 베이스에  이력이 있을 경우 로그인 
                else :
                    # 암호화 토큰생성
                    cursor.close()
                    connection.close()

                    access_token = create_access_token(result_list[0]['id'])

                    return {"result" : "success", "accessToken" : access_token}, 200
            
            
            # 데이터 베이스에 가입정보가 없으면 정보를 저장한다.
            # 닉네임 중복검사
            query = '''select id, nickName, email, password
                    from user
                    where nickName = %s;'''
            
            record = (nickName,)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            # 이미 만들어진 이메일이 있을 때
            if len(result_list) != 0 :
                cursor.close()
                connection.close()
                return {"result" : "중복된 닉네임이 존재 합니다."}, 400
            
            
            # 회원가입
            query = '''insert into user
                        (nickName, email, profileUrl, type)
                        value(%s, %s, %s, 1);'''
            record = (nickName, email, profileUrl)

            # 위에서 한번 사용했기 때문에 커서 초기화 시킨다.
            connection.cursor()
            cursor.execute(query, record)

            
            # 회원가입시 생성한 유저아이디를 데이터베이스에서 가져와
            # 초기 레벨 테이블 정보를 넣어준다.
            userId = cursor.lastrowid

            # level 테이블 생성
            query = '''insert into level
                        (userId)
                        values
                        (%s);'''

            record = (userId,)
            
            # 커서 초기화 
            cursor = connection.cursor()
            cursor.execute(query, record)

            # exercise 테이블 생성
            query = '''insert into exercise
                        (userId)
                        values
                        (%s);'''

            record = (userId,)

            cursor = connection.cursor()
            cursor.execute(query, record)            

            # randomBox 테이블 생성
            query = '''insert into randomBox
                        (userId)
                        values
                        (%s);'''

            record = (userId,)

            cursor = connection.cursor()
            cursor.execute(query, record)  

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"fail" : str(e)}, 500        
        
        # 암호화 토큰생성
        access_token = create_access_token(userId)

        return {"result" : "success", "accessToken" : access_token}, 200

    
jwt_blocklist = set()
class UserLogoutResource(Resource) :            # 로그아웃
    @jwt_required()
    def delete(self) :
        jti = get_jwt()['jti']          # 토큰안에 있는 jti 정보
        print()
        print(jti)
        print()
        jwt_blocklist.add(jti)

        return {"result" : "success"}, 200


