import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

# Constants
TELEFONICA_MIN = 5
TELEFONICA_MAX = 15
ONLINE_MIN = 2
ONLINE_MAX = 10
ESPERA_CITA_MAX = 21 * 24 * 60  # 21 days in minutes
REGISTRO_MIN = 5
REGISTRO_MAX = 10
SALA_ESPERA_MIN = 15
SALA_ESPERA_MAX = 45
CONSULTA_MIN = 10
CONSULTA_MAX = 20
SALIDA_MIN = 5
SALIDA_MAX = 10

# Simulation process
def paciente(env, nombre, metodo_cita):
    
    if metodo_cita == 'telefonica':
        tiempo_solicitud = random.randint(TELEFONICA_MIN, TELEFONICA_MAX)
    else:
        tiempo_solicitud = random.randint(ONLINE_MIN, ONLINE_MAX)
    yield env.timeout(tiempo_solicitud)

 
    tiempo_espera_cita = random.randint(1, 21) * 24 * 60  # Random days up to 21 days
    yield env.timeout(tiempo_espera_cita)


    tiempo_registro = random.randint(REGISTRO_MIN, REGISTRO_MAX)
    yield env.timeout(tiempo_registro)


    tiempo_sala_espera = random.randint(SALA_ESPERA_MIN, SALA_ESPERA_MAX)
    yield env.timeout(tiempo_sala_espera)

    
    tiempo_consulta = random.randint(CONSULTA_MIN, CONSULTA_MAX)
    yield env.timeout(tiempo_consulta)

   
    tiempo_salida = random.randint(SALIDA_MIN, SALIDA_MAX)
    yield env.timeout(tiempo_salida)

   
    tiempos.append({
        'Paciente': nombre,
        'Solicitud de cita': tiempo_solicitud,
        'Espera para la cita': tiempo_espera_cita,
        'Registro': tiempo_registro,
        'Sala de espera': tiempo_sala_espera,
        'Consulta médica': tiempo_consulta,
        'Salida': tiempo_salida,
        'Total': tiempo_solicitud + tiempo_espera_cita + tiempo_registro + tiempo_sala_espera + tiempo_consulta + tiempo_salida,
        'Metodo de cita': metodo_cita
    })


random.seed(42)
env = simpy.Environment()
tiempos = []


NUM_PATIENTS = 300  # Variable to control the number of patients
for i in range(NUM_PATIENTS):
    metodo_cita = random.choice(['telefonica', 'online'])
    env.process(paciente(env, f'Paciente {i+1}', metodo_cita))


env.run()


df = pd.DataFrame(tiempos)


stats = df.describe()


plt.figure(figsize=(10, 6))
plt.hist(df['Total'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribución del Tiempo Total en el Proceso')
plt.xlabel('Tiempo Total (minutos)')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()


colors = ['lightgreen', 'lightcoral', 'lightblue', 'lightpink', 'lightyellow', 'lightgray']
phases = ['Solicitud de cita', 'Espera para la cita', 'Registro', 'Sala de espera', 'Consulta médica', 'Salida']
for i, phase in enumerate(phases):
    plt.figure(figsize=(10, 6))
    if phase == 'Solicitud de cita':
        plt.hist([df[df['Metodo de cita'] == 'telefonica'][phase], df[df['Metodo de cita'] == 'online'][phase]], 
                 bins=20, color=['lightgreen', 'lightblue'], edgecolor='black', label=['Telefonica', 'Online'])
        plt.legend()
    else:
        plt.hist(df[phase], bins=20, color=colors[i], edgecolor='black')
    plt.title(f'Distribución del Tiempo de {phase}')
    plt.xlabel(f'Tiempo de {phase} (minutos)')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()


df.to_csv('reporte_tiempos.csv', index=False)
stats.to_csv('estadisticas_tiempos.csv')


print(stats)
