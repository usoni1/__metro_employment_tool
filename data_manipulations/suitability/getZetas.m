function F = getZetas(inputSOS)
%   Takes in a binary (AREAS x OCCUPATIONS) matrix of specialty flags.

SOS = inputSOS; 
numOccupations = size(SOS,2);
numAreas = size(SOS,1);
zetas = zeros(numOccupations);
    for job1 = 1:numOccupations-1
        for job2 = job1 + 1:numOccupations
             pJob1 = sum(SOS(:,job1)) / numAreas;
             pJob2 = sum(SOS(:,job2)) / numAreas;
             pJoint = sum((SOS(:,job1)+SOS(:,job2))>1) / numAreas;
             zetas(job1,job2) = (pJoint / (pJob1 * pJob2)) - 1;
             zetas(job2,job1) = zetas(job1,job2);
        end
    end
zetas(isnan(zetas)) = 0;      % change any NaN values to 0's
F = zetas;           
end