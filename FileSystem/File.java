package edu.umb.cs.cs680.hw09;

import java.util.Date;

public class File extends FSElement {



	File(Directory parent, String name, String owner, Date created, int size) {
		super(parent, name, owner, created);
		this.size = size;
		System.out.println(name + " created in " + parent.name + " directory ");
	
	}
	
	public boolean isFile() {
		return true;
	}

	public String toString() {

		StringBuffer buffer = new StringBuffer();

		buffer.append("------------------------------------------\r\n");
		buffer.append("File: " + this.name + "\r\n");
		buffer.append("Parent: " + this.parent.name + "\r\n");
		buffer.append("Size: " + this.getSize() + "\r\n");
		buffer.append("Owner: " + this.owner + "\r\n");
		return buffer.toString();
	}
}
