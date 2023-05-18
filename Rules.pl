calculate_density(PoiName,Density) :-
    distance(PoiName, _, Dist),
    Density is Dist.