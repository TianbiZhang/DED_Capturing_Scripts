% This is a sample file combining SmarAct stage motion and PIXET capturing.
% Created by:
% Last edited by Tianbi Zhang

% For the MATLAB version, please navigate MATLAB to the present working directory (the address above the editor), or the python
% code will not be called.
%% Preamble

clear
close all
home

dist_z=100*10; %Distance to move in um
dist_x=1; %in um
exp_num='0'; %number of exposures (n.b. python 0 --> 1 exposure)
acqCount='100'; %number of frames
acqTime='0.05'; %time per frame (s)
n_to_run=50/10; %number of retractions

%% Connect to SmarAct
% convert dist_0 to nm
% dist_0temp = dist_0 * 1000;
% Sort of usb
mcsHandle='usb:id:4199243769'; %Change to the USB port number for the smaract device

% Load the library of C functions for Smaract
if not(libisloaded('MCSControl'))
    loadlibrary('MCSControl.dll','MCSControl.h');
end

[isOpen,o2,o3,o4]=calllib('MCSControl','SA_OpenSystem',1,mcsHandle,'sync');
if isOpen == 0
    disp(['System opened ' int2str(o2)])
end

% Make an array of positions to go to. Positions of each stage occupies a
% row in the array.
positions_n=zeros(3,n_to_run,'int32');

%% Capturing
% Start timing
tic
% Start capturing
try
    % Get initial position 
    % Move the smar act stage in the Z direction (i.e. detector back)
    for n=1:n_to_run
        n
                       
        dist_z_real=-1*dist_z*1000; %Determines direction
        dist_x_real=-1*dist_x*1000; %Determines direction
        
        % Index of channels (stages): 
        % 0 = x, 1 = y, 2 = z by default (Same as MCE Config)
        % Pay attention to the index should you use a different hybrid
        % stage setup!
       
        % Set the target
        % a0 = the status
        % a0=0 means SA_OK, i.e. the function call was successful
        
        % If this does not report 0 (SA_OK) then there was a problem
        % See Appendix 5.1 of the programmer's guide for the meaning of the error code
        [a0]=calllib('MCSControl','SA_GotoPositionRelative_S',o2,2,dist_z_real,1); %MCS,channel,distance,hold_time=0
        [a0]=calllib('MCSControl','SA_GotoPositionRelative_S',o2,0,dist_x_real,1); %MCS,channel,distance,hold_time=0
        
        % Create a directory to store the captured images and log files
        % Change to relative directory, so there is no need to change the directory when running on other computers
        
        % Create and write the log file with file name and camera
        % parameters
        fileID = fopen('C:\Users\tianbi\Documents\DED_script_new\images\dummy.txt','w'); 
        h5_file=['retract_z' sprintf('%03.0f',n)];
        h5_name=['C:\\Users\\tianbi\\Documents\\DED_script_new\\images\\' h5_file]; %file name
        fprintf(fileID, '%s\n%s\n%s\n%s\n', h5_name,exp_num,acqCount,acqTime);
        fclose(fileID);
        
        pause(2); % Pause to let it settle
        
        % Reset the position of the stage
        calllib('MCSControl','SA_GotoPositionAbsolute_S',o2,0,0,1);
        % Get the positions of the stages and record in a vector
        [~,Position_C0]=calllib('MCSControl','SA_GetPosition_S',o2,0,1);
        [~,Position_C1]=calllib('MCSControl','SA_GetPosition_S',o2,1,1);
        [~,Position_C2]=calllib('MCSControl','SA_GetPosition_S',o2,2,1);
        
        positions_n(:,n)=[Position_C0,Position_C1,Position_C2];
        
        % Call the DED capturing py script, stop clock
        % The python script will read parameters from the logfile.
        % Will change this to a more direct path by importing the py script
        % and feed the arguments. Log file will be written separately.
        [r,c]=system('python pyCap2.py');toc

    end
    
    % Prompt keyboard input to retrieve the stage
    k1=input('Please defocus the beam now (CTRL+M on microscope)> [Y] > ','s');
    % A short pause
    pause(2);
    
    % Second for loop, retract camera and capture
    for n=1:n_to_run
        
        % Move stages to positions stored in the position array
        calllib('MCSControl','SA_GotoPositionAbsolute_S',o2,0,positions_n(1,n),60000);
        calllib('MCSControl','SA_GotoPositionAbsolute_S',o2,1,positions_n(2,n),60000);
        calllib('MCSControl','SA_GotoPositionAbsolute_S',o2,2,positions_n(3,n),60000);
        % The holding times look quite long!
        
        % Write patterns into h5 files.
        % Give names to the h5 files. This will be updated each iteration.
        fileID = fopen('C:\Users\tianbi\Documents\DED_script_new\images\dummy.txt','w');
        h5_file=['retract_z_bg' sprintf('%03.0f',n)];
        h5_name=['C:\\Users\\tianbi\\Documents\\DED_script_new\\images\\' h5_file]; %file name
        fprintf(fileID, '%s\n%s\n%s\n%s\n', h5_name,exp_num,acqCount,acqTime);
        fclose(fileID);

        pause(2); %pause to let it settle
        
        [~,Position_C0]=calllib('MCSControl','SA_GetPosition_S',o2,0,1);
        [~,Position_C1]=calllib('MCSControl','SA_GetPosition_S',o2,1,1);
        [~,Position_C2]=calllib('MCSControl','SA_GetPosition_S',o2,2,1);
        
        % What is the purpose of this?
        positions_nbg(:,n)=[Position_C0,Position_C1,Position_C2];


        [r,c]=system('python pyCap2.py');toc
    end
        
    disp('Closing SmarAct');
    [c1]=calllib('MCSControl','SA_CloseSystem',o2);
    disp('Code complete');
    
catch
    disp('Closing SmarAct');
    [c1]=calllib('MCSControl','SA_CloseSystem',o2);
    disp('Code complete');
end