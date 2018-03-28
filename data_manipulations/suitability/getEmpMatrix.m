function F = getEmpMatrix(employmentCellArray)
%getEmpMatrix(employmentCellArray)
% input a cell array of employment (AREA x OCCUPATION) with header column/row.
% Headers are removed and the remaining array is converted to a numeric
% matrix for use in getLQ or other functions.

cellArray = employmentCellArray(2:end,2:end);
emptyIndex = cellfun('isempty',cellArray);          %# Find indices of empty cells
cellArray(emptyIndex) = {0};                        %# Fill empty cells with 0
employmentOut = cell2mat(cellArray);                %# Convert the cell array

F = employmentOut;
end

