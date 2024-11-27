
import time

def temporizador(minutos):
	segundos_totales = minutos * 60

	while segundos_totales > 0:
		minutos_restantes, segundos_restantes = divmod(segundos_totales, 60)
		print(f"{minutos_restantes}:{segundos_restantes}")	
		
		time.sleep(1)
		segundos_totales -= 1