function addline2d(x,y,col='red')
	line([x(1),y(1)],[x(2),y(2)],'Color',col,'LineWidth',2,'LineStyle','-')
end

function addline3d(x,y,col='red')
	line([x(1),y(1)],[x(2),y(2)],[x(3),y(3)],'Color',col,'LineWidth',2,'LineStyle','-')
end


function q = project(p,d=3)
	n = size(p,2);
	q = p(:,(n-d+1):end);
end

function u = rotate3d(v,a,b,c)
	rotx = 	[1	0		0;
			 0	cos(a)	-sin(a); 
			 0 	sin(a)	cos(a)];

	roty = 	[cos(b)		0	sin(b);
			 0			1	0; 
			 -sin(b) 	0	cos(b)];

	rotz = 	[cos(c)	-sin(c)	0;
			 sin(c)	cos(c)	0; 
			 0		0		1];
	u = (rotx*roty*rotz*v')';
end


function rmat = genRotationMatrix(d1,d2,n,alpha)
	mat = eye(n);
	mat(d1,d1) = cos(alpha);
	mat(d2,d2) = cos(alpha);
	mat(d1,d2) = -sin(alpha);
	mat(d2,d1) = sin(alpha);
end

function connectall(P)

	for i=1:8
		for j=(i+1):8
			addline3d(P(i,:),P(j,:))
		end
	end
end


function connectall2d(P)

	for i=1:8
		for j=(i+1):8
			addline2d(P(i,:),P(j,:))
		end
	end
end


function connectadj(P)
	for i=1:size(P,1)
		for j=(i+1):size(P,1)
			v = P(i,:)-P(j,:);
			if nnz(v) == 1
				addline3d(P(i,:),P(j,:))
			end
		end
	end
end

function conMap = createConMap(P)
	conMap = zeros(size(P,1),size(P,1));
	for i=1:size(P,1)
		for j=(i+1):size(P,1)
			v = P(i,:)-P(j,:);
			if nnz(v) == 1
				conMap(i,j) = 1;
			end
		end
	end
end


function connectByConmap3d(P, conMap)
	for i=1:size(P,1)
		for j=(i+1):size(P,1)
			v = P(i,:)-P(j,:);
			if conMap(i,j) == 1
				addline3d(P(i,:),P(j,:))
			end
		end
	end
end

function connectByConmap2d(P, conMap)
	for i=1:size(P,1)
		for j=(i+1):size(P,1)
			v = P(i,:)-P(j,:);
			if conMap(i,j) == 1
				addline2d(P(i,:),P(j,:))
			end
		end
	end
end


P=	[0,0,0;
	 1,0,0;
	 1,1,0;
	 1,1,1;
	 1,0,1;
	 0,1,1;
	 0,0,1;
	 0,1,0;
	 ]

conMap = createConMap(P)


P = rotate3d(P,pi/3,0,pi/7)
P2 = project(P)

%connectByConmap3d(P2, conMap)

%pause

% 4D

P4 = [
0 0 0 0;
0 0 0 1;
0 0 1 0;
0 0 1 1;
0 1 0 0;
0 1 0 1;
0 1 1 0;
0 1 1 1;
1 0 0 0;
1 0 0 1;
1 0 1 0;
1 0 1 1;
1 1 0 0;
1 1 0 1;
1 1 1 0;
1 1 1 1;
]

conMap = createConMap(P4)
P4 = rotate3d(P4,pi/3,0,pi/7)
P3 = project(P4)

connectByConmap3d(P3, conMap)

pause