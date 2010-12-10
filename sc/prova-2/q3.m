simName='q2_sim'

figureIni = 2;

desiredValue = 1;
q=.59921;

k=1;
poles = [-4 -2 -6];
zeros = [];

k = lgrGain(zeros, poles, k, q, figureIni + 1);

sim(simName);

figure(figureIni);
plot(ScopeData.time, ScopeData.signals.values(:,1));
legend('sistema sem controlador');

simLen = length(ScopeData.time);
finalValue = ScopeData.signals.values(simLen,1);
userFinalValue = input(['regime "' num2str(finalValue) '"? [New]']);
if not(isempty(userFinalValue))
    finalValue = userFinalValue;
end
    
err = desiredValue - finalValue;

%equações da apostila pg 78
kp = (1-err) / err;
kpc = 20;
disp(['kp "' num2str(kp) '" kpc "' num2str(kpc) '"']);

poleValue = input('Valor do novo polo? ');
%equação apostila pg 78
zeroValue = (kpc/kp)*poleValue;

disp(['Novo zero "' num2str(zeroValue) '"']);

zeros = horzcat(zeros, zeroValue);
poles = horzcat(poles, poleValue);

k = lgrGain(zeros, poles, 1, q, figureIni+2);

sim(simName)

finalValue = ScopeData.signals.values(simLen,1);
disp(['Novo erro "' num2str(1-finalValue) '"']);

figure(figureIni);
hold;
plot(ScopeData.time, ScopeData.signals.values(:,1), 'r');
hold;
%legend('sistema sem controlador');