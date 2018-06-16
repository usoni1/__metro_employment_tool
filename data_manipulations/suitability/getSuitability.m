% Industry Suitability Index and Ranking

% The suitability algorithm requires 3 sets of data:
%   Industry labor signatures:
%   1. a matrix of employment by occupation by industry for a given country
%
%   Area labor signatures:
%   2. a matrix of employment by occupation by area, for a region of
%   interest (e.g. by city for a whole country, by county for a state, by
%   zip code for a metro area, etc.)
%
%   basis for occupational interdependencies (zetas per Muneepeerakul, et. al, 2013)
%   3. a matrix of employment by occupation by area for a given country
%   (this is typically by metro area for a whole country)
%
%   If the areas of interest are the metro areas of a country, then requirements 2 and 3 will be satisfied by the same matrix
%
%   The vector of occupations must be consistent across all 3 matrices:
%   1. Any occupation present in matrix 1 or 2, but NOT present in matrix 3,
%   should be removed from matrix 1 and 2.  
%   2. Any occupation in matrix 3 but not in matrix 1 or 2 should be added 
%   where missing (with 0 employment)
%   3. Any occupation in matrix 1 or 2, but not in the other, should be
%   added where missing (with 0 employment)


clear, format compact, close all
display('Industry suitability for employment in certain areas')

load('PHX_Suitability_prepped.mat')

% define the 3 matrix requirements
%areaData = MAG_TRP_2015'; % matrix of employment counts by OCC x AREA (e.g. state, MSA, zcta, etc.)
areaData = BLS_OES_2015'; % matrix of employment counts by OCC x AREA (e.g. state, MSA, zcta, etc.)
indData = BLS_NEM_2014'; % matrix of employment counts by OCC x INDUSTRY (e.g. for a country or other deliniations might be used too)
zetaData = BLS_OES_2015'; % matrix of employment counts by OCC x AREA for a whole country (basis of zeta)

% Load basis for calculating zeta (occuapational interdependence)
occCounts = getEmpMatrix(zetaData);
occLQs = getLQs(occCounts);
occSOS = occLQs>1;
zeta = getZetas(occSOS); %Specialized Occupation Set

%% Load labor signatures for geographic areas
areaProfiles = getEmpMatrix(areaData); %gets AREA x OCC matrix of employment counts
areaLQs = getLQs(occCounts); % gets local LQs based on global (e.g. national) totals
areaSOS = areaLQs>1;
areaOccCodes = str2num(cell2mat(areaData(1,2:end)')); %numeric array of OCC codes in the AREA data
areaCodes = str2num(cell2mat(areaData(2:end,1))); %numeric array of local AREA codes

% Load labor signature for industries
indProfiles = getEmpMatrix(indData); %gets IND x OCC matrix of employment counts
indLQs = getLQs(indProfiles); %gets IND x OCC matrix of LQs
indSOS = indLQs>1; %gets binary IND x OCC matrix of specialized occupations (LQ > 1)
indOccCodes = str2num(cell2mat(indData(1,2:end)')); %numeric array of OCC codes in the INDUSTRY data
indCodes = str2num(cell2mat(indData(2:end,1))); %numeric array of INDUSTRY codes

% cycles through the occupation profile for each industry, and then include
% only those occupations' codes that are present in the area profile
for industry = 1:size(indProfiles,1)
%for industry = 1:1
    industry
    indTargets = indOccCodes(find(indSOS(industry,:)==1),1);% getting targets for this particular industry here
    includedThisYr = logical(zeros(size(indTargets)));
    
    for i = 1:length(indTargets)
        if sum(areaOccCodes==indTargets(i))==1 % This code exists that year...
            if sum(areaProfiles(:,areaOccCodes==indTargets(i)))>0 % ...and has some employees - Shade: replaced 'x' with 'empMtrx'
                includedThisYr(i) = 1;
            end
        end
    end
    
    targetOcc = indTargets(includedThisYr);

    %% =============
    targetOccVec = zeros(1,length(areaOccCodes)); % Indicator vector in which occupations part of industry have a 1 and others have a 0
    for i = 1:length(targetOcc)
        targetOccVec(areaOccCodes==targetOcc(i)) = 1;
    end
    NT = sum(targetOccVec); % Total number of 'target' occupations

    %% =============
    commonness = mean(areaSOS); % dot* means elementwise multiplication
    transProb = (zeta+1).*repmat(commonness,size(zeta,1),1); % This is (zeta + 1)P[LQi > 1]
    c = 0.002; % This is the same value used in the PLoS ONE paper.

    %% Set the start and end points: SOSs
    thereIndex = zeros(size(areaProfiles,1),1);
    thereAlready = zeros(size(areaProfiles,1),1);
    therePotential = zeros(size(areaProfiles,1),1);

    for pick = 1:length(thereIndex)
        thereAlready(pick) = sum(areaSOS(pick,:).*targetOccVec);
        here = find(areaSOS(pick,:));
        there = find(targetOccVec==1);
        target = find(~areaSOS(pick,:) & (targetOccVec==1));
        sTransProb = transProb(here,target);
        [easeOfTrans] = 1-prod(1-c*sTransProb); % This is V from Muneepeerakul et al (2013), i.e. ease of transition for each occupation which we want to specialize in individually as an array
        therePotential(pick) = sum(easeOfTrans);
        thereIndex(pick) = (thereAlready(pick) + therePotential(pick));
    end
    %% ===================================
    % [dummyI,dummyRank] = sort(thereIndex,'descend');
    % rankIt = zeros(size(thereIndex));
    % for i = 1:length(rankIt)
    %     rankIt(dummyRank(i)) = i;
    % end

    indProx(:,industry) = thereIndex/NT;
    % indProxNow(:,industry) = thereAlready/NT;
    % indProxPot(:,industry) = therePotential/NT;

end
R = indProx; % this si the final suitability i.e. theta(SOS_zcta -> SOS_ind) AREA X INDUSTRY
RelativeSuitability = bsxfun(@rdivide,bsxfun(@minus,R,mean(R)),std(R)) %convert raw V to relative V or suitability
RelSuit_GlobalBasis = bsxfun(@rdivide,bsxfun(@minus,R,mean(Rglobal)),std(Rglobal))
% the relative suitability for industry I in city M is the I - mean(I) for
% all cities, divided by the standard deviation of I among all cities. Thus
% relative suitability is the number of standard deviations away from the
% mean suitability for a given industry across all cities in a given
% country.
% clear thereIndex rankIt
% save(['CR' yr],'CR','CRnow','CRpot','rankCR','MSAcode')