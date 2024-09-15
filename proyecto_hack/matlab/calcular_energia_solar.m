function energia_generada = calcular_energia_solar(tamano_techo, irradiancia_solar_diaria)
    % Este código calcula la energía solar generada en un día en kWh.
    %
    % tamano_techo: Tamaño del techo en metros cuadrados
    % irradiancia_solar_diaria: Irradiancia solar diaria en kWh/m² (dato obtenido de NASA POWER API)

    % Factor de eficiencia del sistema fotovoltaico (típico entre 15% y 20%)
    eficiencia = 0.18;
    
    % Energía generada en un día
    energia_generada = tamano_techo * irradiancia_solar_diaria * eficiencia;
    
    % Mostrar el resultado
    disp(['Energía solar generada en un día: ', num2str(energia_generada), ' kWh']);
end
