
from database.dao import DAO
p = DAO.read_vertici()

stati = DAO.read_vertici()
archi = DAO.read_archi()

vertici_validi = DAO.read_vertici_validi(2004,'')