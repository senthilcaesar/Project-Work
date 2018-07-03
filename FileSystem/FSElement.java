package edu.umb.cs.cs680.hw09;
import java.util.*;

public class FSElement {

	int size;
	String name, owner;
	Date created, lastModified;
	Directory parent;
	
	FSElement(Directory parent, String name, String owner, Date created){
		
		this.name = name;
		this.owner = owner;
		this.created = created;
		this.parent = parent;
		if (parent != null) {
			this.parent.appendChild(this);
		}
	}
	
	public int getSize() {
		return this.size;
	}
	
	public Directory getParent() {
		return this.parent;
	}
	

}
