package edu.umb.cs.cs680.hw09;

import java.util.Objects;

public class FileSystem {

	private FileSystem() {}
	private static FileSystem base = null;
	public Directory root;
	
	public static FileSystem getInstance(){ // Singleton
		try{
		return Objects.requireNonNull(base);
		}
		catch(NullPointerException ex){
		base = new FileSystem();
		return base;
		} 
	}
	
	public void showAllElements() {
		System.out.println(this.root.toString());
	}
}
