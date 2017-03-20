% % read image and add the mask
img = double(rgb2gray(imread('einst.jpg')))/255;
% %img = img(141:140+256, 51:50+256);
% msk = zeros(size(img));
% msk(65:250,65:250) = imresize(imread('text.png'), 0.7227);
% sz = 185;
% 
% img_corrupted = img;
% img_corrupted(msk > 0) = nan;
img_corrupted = double(rgb2gray(imread('PPCA_corrupted_5.jpg')))/255;
% Corrupted image
% for i=1:size(img, 1);
%     for j=1:size(img,2);
%         if mod(randi(100,1),2)==0
%             img_corrupted(i,j) = nan;
%         end
%     end
% end

fprintf(1, '%d corrupted entries\n', nnz(isnan(img_corrupted)));

%imwrite(img_corrupted, 'img_cor_50.jpg');

% create a matrix X from overlapping patches
ws = 16; % window size
no_patches = size(img, 1) / ws;
X = zeros(no_patches^2, ws^2);

k = 1;
for i = (1:no_patches*2-1)
    for j = (1:no_patches*2-1)
        r1 = 1+(i-1)*ws/2:(i+1)*ws/2;
        r2 = 1+(j-1)*ws/2:(j+1)*ws/2;
        patch = img_corrupted(r1, r2);
        X(k,:) = patch(:);
        k = k + 1;
    end
end

% apply Robust PCA
lambda = 0.02; % close to the default one, but works better
tic
[L, S] = RobustPCA(X, lambda, 1.0, 1e-5);
toc

size(X)

% reconstruct the image from the overlapping patches in matrix L
img_reconstructed = zeros(size(img));
img_noise = zeros(size(img));
k = 1;
for i = (1:no_patches*2-1)
    for j = (1:no_patches*2-1)
        % average patches to get the image back from L and S
        % todo: in the borders less than 4 patches are averaged
        patch = reshape(L(k,:), ws, ws);
        r1 = 1+(i-1)*ws/2:(i+1)*ws/2;
        r2 = 1+(j-1)*ws/2:(j+1)*ws/2;
        img_reconstructed(r1, r2) = img_reconstructed(r1, r2) + 0.25*patch;
        patch = reshape(S(k,:), ws, ws);
        img_noise(r1, r2) = img_noise(r1, r2) + 0.25*patch;
        k = k + 1;
    end
end
img_final = img_reconstructed;
img_final(~isnan(img_corrupted)) = img_corrupted(~isnan(img_corrupted));

% show the results
figure;
subplot(2,1,1), imshow(img_corrupted), title('Missing entries image')
subplot(2,1,2), imshow(img_final), title('Recovered image')
%subplot(2,2,3), imshow(img_reconstructed), title('Recovered low-rank')
%subplot(2,2,4), imshow(img_noise), title('Recovered sparse')

fprintf(1, 'ws=%d\tlambda=%f\trank(L)=%d\tcard(S)=%d\terr=%f\n', ...
       ws, lambda, rank(L), nnz(S), norm(img - img_final, 'fro')/norm(img,'fro'));

   
 percCorr = nnz(isnan(img_corrupted))/(256*256)