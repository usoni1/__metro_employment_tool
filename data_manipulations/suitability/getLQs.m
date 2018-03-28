function F = getLQs(empMatrix, varargin)

%usage getLQs(global employment matrix, optional:local employment matrix)

% Inputs one global (AREA x OCC) matrix of employment counts (without header column/row). 
% Optional: inputs a second local (AREA x OCC) matrix of employment count
% for which LQs will be calculated, using the totals from the first matrix
% in the denominator of the LQ function.
% If 2 matrices are input, they must have the same array of occupation codes.

globalEmp = empMatrix; % Get the global (i.e. national) AREA x OCC count matrix
globalAreaTotals = sum(globalEmp,2); % Get vector of total employment of each global area
globalOccTotals = sum(globalEmp);  % Get vector of total global employment of each occupation
globalTotal = sum(globalOccTotals);% Get total employment of the global area

if length(varargin) == 1
    localEmp = varargin{1};   % Get the local AREA x OCC count matrix, if it is included
    localAreaTotals = sum(localEmp,2); % Get vector of total employment of each local area
    LQ = zeros(size(localEmp));
    for area=1:size(localEmp,1)
        for occ=1:size(localEmp,2)
            LQ(area,occ) = (localEmp(area,occ)/localAreaTotals(area,1)) / (globalOccTotals(1,occ)/globalTotal);
        end
    end
else
    LQ = zeros(size(globalEmp));
    for area=1:size(globalEmp,1)
        for occ=1:size(globalEmp,2)
            LQ(area,occ) = (globalEmp(area,occ)/globalAreaTotals(area,1)) / (globalOccTotals(1,occ)/globalTotal);
        end
    end
end

LQ(isnan(LQ)) = 0;      % change any NaN values to 0's
F = LQ;           
end