from Container import Container
from controller.AppController import AppController
from controller.SetupController import SetupController
from controller.StartController import StartController
from db.repositories.AdresRepository import AdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from db.repositories.PersoonRepository import PersoonRepository
from db.repositories.UserRepository import UserRepository
from manager.GemeenteManager import GemeenteManager
from services.AdresService import AdresService
from services.GemeenteService import GemeenteService
from services.PersoonService import PersoonService
from services.UserService import UserService
from ui.AppUi import appUi

def setup_container():
    container = Container()

    container.set('user_repository', lambda: UserRepository())

    container.set('user_service', lambda: UserService(container.get('user_repository')))

    container.set('gemeente_repository', lambda: GemeenteRepository())
    container.set('gemeente_service', lambda: GemeenteService(container.get('gemeente_repository')))

    container.set('persoon_repository', lambda: PersoonRepository(container.get('gemeente_repository')))
    container.set('persoon_service', lambda: PersoonService(container.get('persoon_repository')))

    container.set('adres_repository', lambda: AdresRepository(container.get('gemeente_repository')))
    container.set('person_adres_repository', lambda: PersoonAdresRepository(

        container.get('adres_repository'),
        container.get('persoon_repository')

    ))

    container.set('adres_service', lambda: AdresService(

        container.get('adres_repository'),
        container.get('person_adres_repository')

    ))

    container.set('gemeente_manager', lambda: GemeenteManager(container.get('gemeente_service')))

    container.set('app_controller', lambda: AppController(container))
    container.set('setup_controller', lambda: SetupController(container.get('app_controller')))
    container.set('start_controller', lambda: StartController(container.get('app_controller')))
    container.set('app_ui', lambda: appUi(container.get('app_controller')))

    return container
