%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%	Instantiation	%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Nodes identification
node(X) :- edge(X,_,_,_).
node(X) :- edge(_,X,_,_).
% Target identification
target(X) :- edge(_,X,_,_).


% Candidate solution generation
0{coloringUp(I)}1 :- node(I).
%#show coloringUp/1.

%Symetric reduction
coloringUp(node0).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%	Constraints	%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Cas de la cohérence
	% Up
consistentTarget(X) :- node(X), coloringUp(X), coloringUp(Y), edge(Y,X,1,_).
consistentTarget(X) :- node(X), coloringUp(X), not coloringUp(Y), edge(Y,X,-1,_).

	% Down
consistentTarget(X) :- node(X), not coloringUp(X), not coloringUp(Y), edge(Y,X,1,_).
consistentTarget(X) :- node(X), not coloringUp(X), coloringUp(Y), edge(Y,X,-1,_).



%Imperfect target coloring
	% up
imperfectcoloring(X) :- coloringUp(X),  not coloringUp(Z), edge(Z,X,1,_).
imperfectcoloring(X) :- coloringUp(X),  coloringUp(Z), edge(Z,X,-1,_).

	% Down
imperfectcoloring(X) :- not coloringUp(X),  coloringUp(Z), edge(Z,X,1,_).
imperfectcoloring(X) :- not coloringUp(X),  not coloringUp(Z), edge(Z,X,-1,_).




% Imperfect weighted regulator
	% up
imperfectWeightedRegulator(X, Y, 1..W) :-  edge(X,Y,1,W), coloringUp(X), not coloringUp(Y).
imperfectWeightedRegulator(X, Y, 1..W) :-  edge(X,Y,-1,W), coloringUp(X), coloringUp(Y).

	% down
imperfectWeightedRegulator(X, Y, 1..W) :-  edge(X,Y,1,W), not coloringUp(X), coloringUp(Y).
imperfectWeightedRegulator(X, Y, 1..W) :-  edge(X,Y,-1,W), not coloringUp(X), not coloringUp(Y).


% Correlation
	% Pos
correlePositif(X,Y) :- coloringUp(X), coloringUp(Y), edge(X,Y,_,_).
correlePositif(X,Y) :- not coloringUp(X), not coloringUp(Y), node(Y), node(X), edge(X,Y,_,_).

	% neg
correleNegatif(X,Y) :- not coloringUp(X), coloringUp(Y), node(X), edge(X,Y,_,_).
correleNegatif(X,Y) :- coloringUp(X), not coloringUp(Y), node(Y), edge(X,Y,_,_).

#show correleNegatif/2.
#show correlePositif/2.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%	Optimization	%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Inconsistency minimization
inconsistentTarget(X) :- not consistentTarget(X), target(X).
sumInconsistencyTargets(X) :- X =#count{ node(Z) :inconsistentTarget(Z) }.
#minimize {X@3 : sumInconsistencyTargets(X)}.

% Imperfect target coloring minimization
sumImperfectcoloring(X) :- X =#count{ node(Z) :imperfectcoloring(Z) }.
#minimize {X@2 : sumImperfectcoloring(X)}.

%  Imperfect weighted regulator minimization
sumImperfectWeightedRegulatorPerTarget(X,Y) :- Y=#count{ x(A, B) : imperfectWeightedRegulator(A,X,B)}, imperfectcoloring(X).

imperfectWeightedRegulatorPerTarget(X,1..W) :- sumImperfectWeightedRegulatorPerTarget(X,W).
sumImperfectWeightedRegulator(X) :- X=#count{ x(Y,Z) : imperfectWeightedRegulatorPerTarget(Y,Z),imperfectcoloring(Y)}.
#minimize {X@1 : sumImperfectWeightedRegulator(X)}.


%clingo graphePoidsCompacte.lp scriptASPIntersections/optimizationComponent.lp  -n 0 -t 3 --opt-mode=optN
%clingo graphePoidsCompacte.lp scriptASPIntersections/optimizationComponent.lp -n 0 -t 3 --opt-mode=optN --enum-mode=cautious --quiet=1




