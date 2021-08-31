import logging
import traceback
from datetime import datetime, date
from getpass import getpass
from save_money.services import SaveMoneyService
from save_money.models import UserAuth, Token, Movimentation
import config


class Integrator:

    def __init__(self):
        self.sm_service = SaveMoneyService()
        try:
            self.compose()
        except Exception as e:
            logging.error(traceback.format_exc())
            raise

    def compose(self):
        self.get_token()
        self.get_categories()
        movimentations = self.read_nu_movimentations()
        self.save_movimentations(movimentations)

    def get_user_auth(self):
        username = config.SAVE_MONEY_USERNAME or input('E-mail')
        password = config.SAVE_MONEY_PASSWORD or getpass()
        return UserAuth(username, password)

    def get_token(self):
        user = self.get_user_auth()
        logging.info(f"Get auth to {user.username}")
        token = self.sm_service.get_token(user)
        self.sm_service.set_authorization(jwt='Bearer '+ token.access_token)

    def get_categories(self):
        self.categories = self.sm_service.get_categories()
        print(self.categories)
        logging.info(f"Get {len(self.categories)} Categories")
    
    def read_nu_movimentations(self):
        logging.info('Read movimentations on nubank')
        return [Movimentation(
            is_expense=True,
            title='Pizza',
            value=5.00,
            description='',
            category=8,
            number_of_installments=1,
            efetivation_date=date.today(),
            tags=['NuBank']
        )]

    def save_movimentations(self, movimentations):
        # TODO: create route to save list of movimentations 
        for movimentation in movimentations:
            logging.info(f"Save {movimentation.title}")
            self.sm_service.create_movimentation(movimentation)

if __name__ == '__main__':
    logging.basicConfig(
        # filename=f"logs/sm_nu_{datetime.now().strftime('%d_%m_%y_%H_%M')}.log",
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%d/%m/%y %H:%M',
        level=logging.INFO
    )
    Integrator()    
