% Función para calcular reducción de CO2 para energía eólica
function reduccion_co2 = calcular_reduccion_co2_eolica(energia_generada)
    % Factores de emisión (en toneladas de CO2 por kWh)
    factor_emision_co2 = 0.707; % kilogramos de CO2 por kWh
    reduccion_co2 = energia_generada * factor_emision_co2;
end