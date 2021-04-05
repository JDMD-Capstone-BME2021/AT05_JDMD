function out = circuitControl(port_name, delay_time,steps, speed)
%circuitControl fcn to execute 
%motor control and light control modules
%for Arduino UNO, default voltage is 5.0V

arguments
    port_name = 'COM4';
    delay_time = 1000;
    steps = 100;
    baudRate = 9600;
    mcu_type = 'Uno';
end

%open the port
s1 = serial(port_name, mcu_type);
fopen(s1=),% open the serial port

%set pins
blue = configurePin(a, 'A0', DigitalInput);
green = configurePin(a, 'A1', DigitalInput);
red = configurePin(a, 'A2', DigitalInput);

%code implementation
a = arduino(port_name, mcu_type);
while(1)
    %light emission 
    writeDigitalPin(a, blue, 1);
    pause(delay_time);
    writeDigitalPin(a, green, 1);
    pause(delay_time);
    writeDigitalPin(a, red, 1);
    pause(delay_time);
end

fclose(s1) %close the serial port
delete(s1)
clear s1

end

