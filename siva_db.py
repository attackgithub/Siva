# SWAMI KARUPPASWAMI THUNNAI

# ===============================================
# UNIT TEST THIS CLASS LIKE ANYTHING IN THE WORLD
# ===============================================

from url.URL import URL
import pymysql
import getpass


class SivaDB:
    """
    This class will be the one and the only class which is used to perform database related operations
    """

    # This method will be called as a command line argument e.g ./siva.py install
    def install(self):
        """
        This method is used to install the database
        :return: True if the database has been installed successfully
        """
        user_name = input("USER NAME: ")
        password = getpass.getpass()
        connection = pymysql.connect(
            host="localhost", user=user_name, password=password)
        cursor = connection.cursor()
        print("[+] CREATING A DATABASE")
        cursor.execute("create database if not exists siva")
        cursor.execute("use siva")
        ports_table = "create table if not exists port(project_id int(10), port_no int(6))"
        raw_info_table = "create table if not exists raw_information(project_id int(10), info_source varchar(1000), information longtext)"
        admin_page_table = "create table if not exists admin_page(project_id int(10), url varchar(1000))"
        analysis_table = "create table if not exists analysis(project_id int(10), method varchar(10), source varchar(1000), payload varchar(1000), description varchar(1000))"
        print("[+] CREATING PORTS TABLE")
        self.execute_query(connection, ports_table)
        print("[+] CREATING RAW INFO TABLE")
        self.execute_query(connection, raw_info_table)
        print("[+] CREATING ADMIN PAGE")
        self.execute_query(connection, admin_page_table)
        print("[+] CREATING INFO GATHERING TABLE")
        self.execute_query(
            connection,
            "create table if not exists info_gathering(project_id int(10) primary key, status varchar(100), ip varchar(100), webserver_name varchar(100), server_os varchar(100), programming_language varchar(150), firewall_name varchar(100));"
        )
        print("[+] CREATING PROJECTS TABLE")
        self.execute_query(
            connection,
            "create table if not exists project(project_id int(10) primary key, domain varchar(1000))"
        )
        print("[+] CREATING RESULT TABLE")
        self.execute_query(
            connection,
            "create table if not exists result(project_id int(10), phase_name varchar(30))"
        )
        print("[+] CREATING ANALYSIS TABLE")
        self.execute_query(connection, analysis_table)
        print("[+] SIVA HAS BEEN INSTALLED")

    def execute_query(self, connection, query):
        """
        Dexcription:
        ============
        This method will blindly execute the data_stores query so use it carefully.
        Parameters:
        ===========
        :param cursor: pymysql cursor object
        :param query: the query to be executed
        :return:
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("[+] QUERY EXECUTED SUCCESSFULLY.")

    @staticmethod
    def create_project(connection, project_id, url):
        """
        Description:
        =============
        This method is used to create the project, and the project id
        :param connection: The database connection object
        :param project_id: The id of the project
        :param url: The url of the project
        :return: True if the process is competed else false
        """
        try:
            cursor = connection.cursor()
            cursor.execute("insert into project values(%s, %s)",
                           (project_id, URL().get_host_name(url)))
            connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_result(connection, project_id, phase_id):
        """
        Description:
        ============
        This method is used to update the status that which phase is currently completed
        :param connection:
        :param project_id:
        :param result_status:
        :return: True if the staus is updated
        """
        try:
            cursor = connection.cursor()
            cursor.execute("insert into result values(%s, %s)",
                           (project_id, phase_id))
            connection.commit()
            print("[+] RESULT UPDATED")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_raw_info(connection, project_id, info_source, information,
                        database_semaphore):
        """
        Description:
        ============
        This method is used to update the status that which phase is currently completed
        :param connection:
        :param project_id:
        :param result_status:
        :return: True if the staus is updated
        """
        database_semaphore.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute("insert into raw_information values(%s, %s, %s)",
                           (project_id, info_source, information))
            connection.commit()
            print("[+] RAW INFORMATION UPDATED")
            return True
        except Exception as e:
            print(e)
            return False
        database_semaphore.release()

    @staticmethod
    def update_analysis(connection, database_semaphore, project_id, method,
                        source, payload, description):
        database_semaphore.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute("insert into analysis values(%s, %s, %s, %s, %s)",
                           (project_id, method, source, payload, description))
            connection.commit()
            print("[+] RAW INFORMATION UPDATED")
            return True
        except Exception as e:
            print(e)
            return False
        database_semaphore.release()
