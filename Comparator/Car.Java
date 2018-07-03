package edu.umb.cs.cs680.hw06;

import java.util.List;

public class Car {

	int price, year, dominationCount;
	double mileage;
	
	Car(int price, int year, double mileage){
		
		this.price   = price;
		this.year    = year;
		this.mileage = mileage;
	}
	
	public int    getPrice()   			{return this.price;}
	public int    getYear()    			{return this.year;}
	public double getMileage() 			{return this.mileage;}
	public int    getDominationCount()  {return this.dominationCount;}
	
	public int computeDominationCount(Car c1, List<Car> usedCars)  {
		
		for(int k = 0; k < usedCars.size(); k++) { 
			
			if(!c1.equals(usedCars.get(k))) {
				
				//System.out.println(c1.price + " >= " + usedCars.get(k).price);
				//System.out.println(c1.mileage + " >= " + usedCars.get(k).mileage);
				
					if(c1.price >= usedCars.get(k).price || c1.mileage >= usedCars.get(k).mileage) { 
						dominationCount++; 
			     }
			} 
		}
		return this.dominationCount;
	}
	
	
	
	
}
