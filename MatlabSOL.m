clc; close all; clear;
format long g
sheet4 = xlsread('ASC.xlsx', 4); 
data = sheet4(:,4)';
numWeeks = 52; 
yearIndex = 1; 
yearScaler = 1 + 0.1*yearIndex;
r1CutOff = 2540/0.12;
r2CutOff = 1640/0.07;
r3CutOff = 1200/0.07;
r4CutOff = 1200/0.06;

numHammers = 0;
transportSum_A = 0;

for weekIndex = 1:numWeeks
    orderQty = data((weekIndex-1)*6+1:weekIndex*6);
    r1 = (4.2*orderQty(1) + 1.2*orderQty(2))*yearScaler;
    r2 = (4.2*orderQty(3) + 1.2*orderQty(4))*yearScaler;
    r3 = 8.3*orderQty(5)*yearScaler;
    r4 = 8.3*orderQty(6)*yearScaler;
    numHammers = ceil(numHammers + (orderQty(1) + orderQty(3))*yearScaler);
    
    if (r1 > 44000 || r2 > 44000 || r3 > 44000 || r4 > 44000)
        error('Model A supply flow too large!');
    end
    
    if ((0 <= r1) && (r1 <= r1CutOff))
        transportSum_A = transportSum_A + r1*0.12;
    else
        transportSum_A = transportSum_A + 2540;
    end
    
    if ((0 <= r2) && (r2 <= r2CutOff))
        transportSum_A = transportSum_A + r2*0.07;
    else
        transportSum_A = transportSum_A + 1640;
    end
    
    if ((0 <= r3) && (r3 <= r3CutOff))
        transportSum_A = transportSum_A + r3*0.07;
    else
        transportSum_A = transportSum_A + 1200;
    end
    
    if ((0 <= r4) && (r4 <= r4CutOff))
        transportSum_A = transportSum_A + r4*0.06;
    else
        transportSum_A = transportSum_A + 1200;
    end
end

hammerProductionCost_A = 0.80*numHammers; 
totalCost_A = transportSum_A + hammerProductionCost_A; 

transportSum_B = 0;

for weekIndex = 1:numWeeks
    orderQty = data((weekIndex-1)*6+1:weekIndex*6);
    r1 = (2.2*orderQty(1) + 1.2*orderQty(2))*yearScaler;
    r2 = (2.2*orderQty(3) + 1.2*orderQty(4))*yearScaler;
    r3 = (8.3*orderQty(5) + 2*orderQty(1))*yearScaler;
    r4 = (8.3*orderQty(6) + 2*orderQty(3))*yearScaler;
    
    if (r1 > 44000 || r2 > 44000 || r3 > 44000 || r4 > 44000)
        error('Model B supply flow too large!');
    end
    
    if ((0 <= r1) && (r1 <= r1CutOff))
        transportSum_B = transportSum_B + r1*0.12;
    else
        transportSum_B = transportSum_B + 2540;
    end
    
    if ((0 <= r2) && (r2 <= r2CutOff))
        transportSum_B = transportSum_B + r2*0.07;
    else
        transportSum_B = transportSum_B + 1640;
    end
    
    if ((0 <= r3) && (r3 <= r3CutOff))
        transportSum_B = transportSum_B + r3*0.07;
    else
        transportSum_B = transportSum_B + 1200;
    end
    
    if ((0 <= r4) && (r4 <= r4CutOff))
        transportSum_B = transportSum_B + r4*0.06;
    else
        transportSum_B = transportSum_B + 1200;
    end
end

hammerProductionCost_B = 0.82*numHammers; 
totalCost_B = transportSum_B + hammerProductionCost_B; 


if totalCost_B > totalCost_A
    disp('Supplier A is the cost effective choice.');
else
    disp('Supplier B is the cost effective choice.');
end

fprintf('The total cost for model A is: %0.5f. \nThe total cost for model B is: %0.5f.\n', totalCost_A, totalCost_B);
numHammers