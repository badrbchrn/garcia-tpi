"""Contient la classe de contrôle des utilisateurs

@author: Tanguy Cavagna
@copyright: Copyright 2020, TPI
@version: 1.0.0
@date: 2020-05-05
"""
from .SqliteController import SqliteController
from .RoleController import RoleController
from ..models.User import User

class UserController:

    def __init__(self):
        pass
        
    def insert(self, email: str, password: str, last_name: str, first_name: str, phone: str) -> User:
        """Insère un nouvel utilisateur
        
            Arguments:
                email {string} -- Email
                password {string} -- Mot de passe
                last_name {string} -- Nom
                first_name {string} -- Prénom
                phone {string} -- Télephone
            
            Returns:
                User -- Utilisateur inscrit
        """
        sql_insert = "INSERT INTO user(lastnameUser, firstnameUser, emailUser, passwordUser, phoneUser, idRole) VALUES(?, ?, ?, ?, ?, ?)"

        values_user = (
            last_name,
            first_name,
            email,
            password,
            phone,
            RoleController().get_default().id
        )

        last_row_id = SqliteController().execute(sql_insert, values=values_user)

        return User(last_row_id, last_name, first_name, email, phone, RoleController().get_default())

    def exists(self, email: str) -> bool:
        """Test si l'email existe deja en base
            
            Arguments:
                email {str} -- Email à tester
            
            Returns:
                bool -- True si deja existant, False sinon
        """
        sql_exists = "SELECT COUNT(*) AS `Count` FROM user WHERE emailUser = ?"

        count = SqliteController().execute(sql_exists, values=(email, ), fetch_mode=SqliteController.FETCH_ONE)['Count']

        return True if count > 0 else False

    def check_password(self, email: str, hashed_password: str) -> bool:
        """Test la validité du mot de passe entré
        
            Arguments:
                email {str} -- Email de l'utilisateur
                hashed_password {str} -- Mot de passe à tester
            
            Returns:
                bool -- True si mot de passe valide, sinon False
        """
        sql_check = "SELECT COUNT(*) AS `Count` FROM user WHERE emailUser = ? AND passwordUser = ?"

        count = SqliteController().execute(sql_check, values=(email, hashed_password, ), fetch_mode=SqliteController.FETCH_ONE)['Count']

        return True if count == 1 else False

    def get_by_email(self, email: str) -> User:
        """Récupère l'utilisateur via son email
        
            Arguments:
                user_id {str} -- Email de l'utilisateur cherché
            
            Returns:
                User -- Utilisateur trouvé
        """
        sql_select = "SELECT * FROM user WHERE emailUser = ?"

        user_dict = SqliteController().execute(sql_select, values=(email, ), fetch_mode=SqliteController.FETCH_ONE)

        if user_dict is not None:
            return User(user_dict['idUser'], user_dict['lastnameUser'], user_dict['firstnameUser'], user_dict['emailUser'], user_dict['phoneUser'], RoleController().get_by_id(user_dict['idRole']))
        else:
            return None

    def get_by_id(self, user_id: int) -> User:
        """Récupère l'utilisateur via son email
        
            Arguments:
                user_id {int} -- Id de l'utilsiateur cherché
            
            Returns:
                User -- Utilisateur trouvé
        """
        sql_select = "SELECT * FROM user WHERE idUser = ?"

        user_dict = SqliteController().execute(sql_select, values=(user_id, ), fetch_mode=SqliteController.FETCH_ONE)

        if user_dict is not None:
            return User(user_dict['idUser'], user_dict['lastnameUser'], user_dict['firstnameUser'], user_dict['emailUser'], user_dict['phoneUser'], RoleController().get_by_id(user_dict['idRole']))
        else:
            return None

    def get_all(self) -> [User]:
        """Retourne la liste de tous les utilisateur

            Returns:
                [User] -- Liste des utilisateurs
        """
        try:
            sql_select = "SELECT * FROM user"

            rows = SqliteController().execute(sql_select, fetch_mode=SqliteController.FETCH_ALL)

            return [User(r['idUser'], r['lastnameUser'], r['firstnameUser'], r['emailUser'], r['phoneUser'], RoleController().get_by_id(r['idRole'])) for r in rows]
        except Exception as e:
            raise e

    def set_by_id(self, user_id: int, email: str, last_name: str, first_name: str, phone: str) -> bool:
        """Met à jour les données d'un utilisateur

            Arguments:
                user_id {int} -- Id
                email {str} -- Email
                last_name {str} -- Nom
                first_name {str} -- Prénom
                phone {str} -- Téléphone
            
            Returns:
                bool -- Status de l'update
        """
        try:
            sql_update = "UPDATE user SET emailUser = ?, lastnameUser = ?, firstnameUser = ?, phoneUser = ? WHERE idUser = ?"

            status = SqliteController().execute(sql_update, values=(email, last_name, first_name, phone, user_id,))

            return True if status != None else False
        except Exception as e:
            raise e

    def delete_by_id(self, user_id: int) -> bool:
        """Supprime un utiliateur

            Arguments:
                user_id {int} -- Id
            
            Returns:
                bool -- Status de la suppression
        """
        try:
            sql_delete = "DELETE FROM user WHERE idUser = ?"

            status = SqliteController().execute(sql_delete, values=(user_id,))

            return True if status == None else False
        except Exception as e:
            raise e
