import java.io.*;
import java.net.*;

public class PrisioneroCliente {
    public static void main(String[] args) {
        String host = "192.168.63.61";
        int puerto = 5000;

        try (Socket socket = new Socket(host, puerto)) {
            System.out.println("Conectado al servidor.");

            // Flujo de entrada y salida
            BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter salida = new PrintWriter(socket.getOutputStream(), true);

            // Recibir percepción del Equipo 1
            String percepcion1 = entrada.readLine();
            System.out.println("El Equipo 1 uno los percibe como: " + percepcion1);

            // Equipo 2 elige su percepción
            BufferedReader lector = new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Equipo 2, ¿cómo perciben al Equipo 1? (amigo/x/cae mal): ");
            String percepcion2 = lector.readLine().trim().toLowerCase();
            salida.println(percepcion2);

            // Equipo 2 elige su estrategia
            System.out.println("Equipo 2, elijan su estrategia (cooperar/traicionar): ");
            String estrategia2 = lector.readLine().trim().toLowerCase();
            salida.println(estrategia2);

            // Recibir estrategia del Equipo 1
            String estrategia1 = entrada.readLine();
            System.out.println("Decisión del Equipo 1 recibida.");

            // Evaluar resultados
            String resultados = evaluarResultados(estrategia1, estrategia2);
            System.out.println("\nResultados finales:");
            System.out.println(resultados);
            System.out.println("\n¡Profe Mark lo queremos!");

        } catch (IOException e) {
            System.err.println("Error en el cliente: " + e.getMessage());
        }
    }

    private static String evaluarResultados(String equipo1, String equipo2) {
        if (equipo1.equals("cooperar") && equipo2.equals("cooperar")) {
            return "Ambos equipos cooperaron. ¡Ambos sacan 10 puntos!";
        } else if (equipo1.equals("traicionar") && equipo2.equals("cooperar")) {
            return "Equipo 1 traicionó y Equipo 2 cooperó.\nEquipo 1: 10 puntos + 5 puntos extra + 1 práctica exentada.\nEquipo 2: 7 puntos.";
        } else if (equipo1.equals("cooperar") && equipo2.equals("traicionar")) {
            return "Equipo 2 traicionó y Equipo 1 cooperó.\nEquipo 2: 10 puntos + 5 puntos extra + 1 práctica exentada.\nEquipo 1: 7 puntos.";
        } else if (equipo1.equals("traicionar") && equipo2.equals("traicionar")) {
            return "Ambos equipos se traicionaron.\nAmbos pierden sus puntos extra y solo sacan 6 puntos cada uno.";
        } else {
            return "Entrada no válida. Asegúrate de que ambos equipos escriban 'cooperar' o 'traicionar'.";
        }
    }
}