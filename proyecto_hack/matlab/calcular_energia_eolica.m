function energia_generada = calcular_energia_eolica(tamano_techo, velocidad_viento)
    % Este código calcula la energía eólica generada en un día.
    %
    % tamano_techo: Área disponible en metros cuadrados para las turbinas eólicas
    % velocidad_viento: Velocidad del viento en m/s (dato obtenido de NASA POWER API)

    % Densidad del aire en kg/m³ (valor típico)
    densidad_aire = 1.225;
    
    % Coeficiente de potencia de la turbina (típico entre 0.3 y 0.5)
    coeficiente_potencia = 0.4;
    
    % Área del rotor (depende del tamaño de las aspas, en este caso simplificada al tamaño del techo)
    area_rotor = tamano_techo;  % Suposición simple para la demo
    
    % Energía eólica disponible (potencia en W)
    potencia_viento = 0.5 * densidad_aire * area_rotor * coeficiente_potencia * (velocidad_viento^3);
    
    % Convertir potencia a kWh por día (multiplicar por 24 horas y dividir por 1000 para kW)
    energia_generada = (potencia_viento * 24) / 1000;
    
    % Mostrar el resultado
    disp(['Energía eólica generada en un día: ', num2str(energia_generada), ' kWh']);
end