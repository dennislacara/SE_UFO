
from database.dao import DAO


stati = DAO.read_vertici()
archi = DAO.read_archi()

vertici_validi = DAO.read_vertici_validi(2004,'')