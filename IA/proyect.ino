#include <avr/io.h>
#include <avr/interrupt.h>

// Configuración de UART
void UART_Init(unsigned int baud) {
    unsigned int ubrr = F_CPU / 16 / baud - 1;
    UBRR0H = (unsigned char)(ubrr >> 8);
    UBRR0L = (unsigned char)ubrr;
    UCSR0B = (1 << RXEN0) | (1 << TXEN0); // Habilitar RX y TX
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); // Modo 8 bits
}

unsigned char UART_Receive() {
    while (!(UCSR0A & (1 << RXC0))); // Esperar a recibir
    return UDR0;
}

// Configuración de SPI para MAX7219
#define DD_MOSI PB3
#define DD_SCK PB5
#define DD_SS PB2
#define DDR_SPI DDRB
#define PORT_SPI PORTB

void SPI_MasterInit(void) {
    DDR_SPI = (1 << DD_MOSI) | (1 << DD_SCK) | (1 << DD_SS);
    SPCR = (1 << SPE) | (1 << MSTR) | (1 << SPR0);
}

void SPI_MasterTransmit(char cData) {
    SPDR = cData;
    while (!(SPSR & (1 << SPIF)));
}

void MAX7219_Send(uint8_t address, uint8_t data) {
    PORT_SPI &= ~(1 << DD_SS); // CS en bajo
    SPI_MasterTransmit(address);
    SPI_MasterTransmit(data);
    PORT_SPI |= (1 << DD_SS); // CS en alto
}

void MAX7219_Init() {
    MAX7219_Send(0x0B, 0x07); // Configurar 8 dígitos
    MAX7219_Send(0x09, 0x00); // Sin decodificación
    MAX7219_Send(0x0A, 0x05); // Intensidad (puedes cambiar entre 0x00 y 0x0F)
    MAX7219_Send(0x0C, 0x01); // Salir de shutdown
    MAX7219_Send(0x0F, 0x00); // Modo normal
}

// Números de 4 columnas de ancho
uint8_t numbers[10][8] = {
    {0b0110, 0b1001, 0b1001, 0b1001, 0b1001, 0b1001, 0b0110, 0b0000}, // 0
    {0b0010, 0b0110, 0b0010, 0b0010, 0b0010, 0b0010, 0b0111, 0b0000}, // 1
    {0b0110, 0b1001, 0b0001, 0b0010, 0b0100, 0b1000, 0b1111, 0b0000}, // 2
    {0b0110, 0b1001, 0b0001, 0b0110, 0b0001, 0b1001, 0b0110, 0b0000}, // 3
    {0b0001, 0b0011, 0b0101, 0b1001, 0b1111, 0b0001, 0b0001, 0b0000}, // 4
    {0b1111, 0b1000, 0b1110, 0b0001, 0b0001, 0b1001, 0b0110, 0b0000}, // 5
    {0b0110, 0b1001, 0b1000, 0b1110, 0b1001, 0b1001, 0b0110, 0b0000}, // 6
    {0b1111, 0b0001, 0b0010, 0b0010, 0b0100, 0b0100, 0b0100, 0b0000}, // 7
    {0b0110, 0b1001, 0b1001, 0b0110, 0b1001, 0b1001, 0b0110, 0b0000}, // 8
    {0b0110, 0b1001, 0b1001, 0b0111, 0b0001, 0b1001, 0b0110, 0b0000}  // 9
};

// Mostrar el número de dos dígitos con unidades y decenas invertidas
void MAX7219_DisplayTwoDigits(uint8_t value) {
    uint8_t tens = value / 10;  // Decenas
    uint8_t units = value % 10; // Unidades

    for (uint8_t i = 0; i < 8; i++) {
        // Intercambiar el orden de unidades y decenas
        uint8_t combined = (numbers[tens][i] << 4) | (numbers[units][i]);
        MAX7219_Send(i + 1, combined);
    }
}

// Configuración de PWM para Servo
void PWM_Init() {
    DDRB |= (1 << PB1); // Configurar PB1 (OC1A) como salida
    TCCR1A = (1 << COM1A1) | (1 << WGM11); // PWM no inverso, modo rápido
    TCCR1B = (1 << WGM12) | (1 << WGM13) | (1 << CS11); // Prescaler 8
    ICR1 = 20000; // 20 ms para servo estándar
}

int16_t currentAngle = 0;  // Ángulo actual del servomotor

void Servo_SetPosition(int8_t angle) {
    // Validar que el ángulo esté en el rango esperado
    if (angle < -90) angle = -90;
    if (angle > 90) angle = 90;

    // Mapear el ángulo al valor PWM correcto
    //int16_t pwmValue = 500 + ((int32_t)(angle + 90) * (2500 - 500)) / 180;
    int pwmValue = map(angle, -90, 90, 544, 2400);

    // Configurar el registro de comparación del PWM
    OCR1A = pwmValue;

    // Actualizar el ángulo actual
    currentAngle = angle;
}


// Función para mover suavemente el servo desde el ángulo actual al ángulo objetivo
void MoveServoSmoothly(int8_t targetAngle) {
    // Determinar la dirección del movimiento
    int8_t step = (targetAngle > currentAngle) ? 1 : -1;

    // Mover el servo gradualmente hasta alcanzar el ángulo objetivo
    while (currentAngle != targetAngle) {
        currentAngle += step; // Incrementar o decrementar el ángulo
        Servo_SetPosition(currentAngle); // Ajustar el servo según el nuevo ángulo
        _delay_ms(10); // Pequeña pausa para un movimiento suave
    }
}

// Función para convertir valor a ángulo
int8_t ValueToAngle(uint8_t value) {
    // Map the range [0, 99] to [-90, 90]
    return (int8_t)((value * 180) / 99) - 90;
}

int main(void) {
    UART_Init(9600);       // Inicializar UART
    SPI_MasterInit();      // Inicializar SPI
    MAX7219_Init();        // Inicializar MAX7219
    PWM_Init();            // Inicializar PWM
    Serial.begin(9600);    // Inicializar Serial para depuración

    uint8_t receivedValue = 0;
    uint8_t displayValue = 0;

    while (1) {
        // Leer valor de UART
        receivedValue = UART_Receive();
        
        if (receivedValue >= '0' && receivedValue <= '9') {
            uint8_t tens = UART_Receive() - '0'; // Leer siguiente dígito
            displayValue = (receivedValue - '0') * 10 + tens;
            receivedValue = displayValue; // Correct order for servo

            if (displayValue <= 99) {
                MAX7219_DisplayTwoDigits(displayValue); // Mostrar número con unidades y decenas invertidas
                int8_t angle = ValueToAngle(receivedValue); // Convertir valor a ángulo
                Serial.print("Valor recibido: ");
                Serial.print(receivedValue);
                Serial.print(" | Ángulo calculado: ");
                Serial.println(angle); // Imprime el valor recibido y el ángulo calculado
                MoveServoSmoothly(angle); // Mover el servo suavemente al ángulo calculado
            }
        }
    }

    return 0;
}
