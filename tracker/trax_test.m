function [supported] = trax_test(tracker)
% trax_test Test support for TraX protocol
%
% This function runs the traxclient executable in a query mode to test
% if a tracker supports the TraX protocol. The results are chached
% in the workspace cache directory.
%
% Input:
% - tracker: Tracker structure.
%
% Output:
% - supported (boolean): Is the protocol supported.

trax_executable = get_global_variable('trax_client', '');

if isempty(trax_executable)
    error('TraX support not available');
end;

% Check if the result of the test is already cached

cache = fullfile(get_global_variable('directory'), 'cache', 'trax');

tracker_hash = md5hash(sprintf('%s-%s-%s', tracker.command, tracker.interpreter, strjoin(tracker.linkpath, '-')));
    
mkpath(cache);
    
cache_file = fullfile(cache, sprintf('trax_%s_%s.mat', tracker.identifier, tracker_hash));

supported = [];
if exist(cache_file, 'file')         
    load(cache_file);
    if ~isempty(supported)
        return;
    end;
end; 

debug = get_global_variable('trax_debug', false);

print_text('Testing TraX protocol support for tracker %s.', tracker.identifier);

arguments = '-Q'; % Use query mode of traxclient

if debug
    arguments = [arguments, ' -d'];
end;

% Specify timeout period
timeout = get_global_variable('trax_timeout', 30);
arguments = [arguments, sprintf(' -t %d', timeout)];

% Hint to tracker that it should use trax
arguments = [arguments, ' -e "TRAX=1"'];

% If we are running Matlab tracker on Windows or Python we have to use TCP/IP
% sockets
if (ispc && strcmpi(tracker.interpreter, 'matlab')) || strcmpi(tracker.interpreter, 'python')
    arguments = [arguments, ' -X'];
end



if ispc
command = sprintf('"%s" %s -- %s', trax_executable, ...
    arguments, tracker.command);
else
command = sprintf('%s %s -- %s', trax_executable, ...
    arguments, tracker.command);
end

library_path = '';

if ispc
    library_var = 'PATH';
else
    library_var = 'LD_LIBRARY_PATH';
end;

try
    print_debug(['INFO: Executing "', command, '".']);

    % Save library paths
    library_path = getenv(library_var);

    % Make Matlab use system libraries
    if ~isempty(tracker.linkpath)
        userpath = strjoin(tracker.linkpath, pathsep);
        setenv(library_var, [userpath, pathsep, getenv('PATH')]);
    else
        setenv(library_var, getenv('PATH'));
    end;
    
    if is_octave()

        [status, output] = system(command, 1);
    else

		if verLessThan('matlab', '7.14.0')
		    [status, output] = system(command);
        else
		    [status, output] = system(command, '');
		end;
    end;

    supported = true;
    if status ~= 0 

        supported = false;
    
    end;

    if debug
        print_text('Printing client output:');
        print_text('-------------------- Begin raw output ------------------------');
        % This prevents printing of backspaces and such
        disp(output(output > 31 | output == 10 | output == 13));
        print_text('--------------------- End raw output -------------------------');
    end;

catch e

	% Reassign old library paths if necessary
	if ~isempty(library_path)
		setenv(library_var, library_path);
	end;

    print_debug('ERROR: Exception thrown "%s".', e.message);
end;

save(cache_file, 'supported', 'status', 'output');

if supported
    print_text('TraX support is present.');
else
	print_text('TraX support is not present.');
end

end
