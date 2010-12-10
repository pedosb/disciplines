function [newGain] = lgrGain(zeros, poles, gain, q, figureId);

figure(figureId);
q2 = zpk(zeros, poles, gain)
rlocus(q2);
sgrid(q, '');

k = input('ganho? ');

newGain = k;

end