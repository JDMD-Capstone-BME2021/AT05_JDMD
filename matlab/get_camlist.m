function results = get_camlist()
%GET_CAMLIST Returns list of available cameras
n = length(webcamlist);
results = strings([n 1]);
for i = 1:n
    results(i) = webcam(i).Name;
end
end

