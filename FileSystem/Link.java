package edu.umb.cs.cs680.hw09;

import java.util.Date;

public class Link extends FSElement {

	private FSElement target;
	Link(Directory parent, String name, String owner, Date created, FSElement link) {
		super(parent, name, owner, created);
		this.size = 0;
		this.target = link;
		System.out.println(name + " pointing to " + this.target.name);
	}

	public int getTargetSize() {
		return this.target.size;
	}
	
	public String toString() {

		StringBuffer buffer = new StringBuffer();

		buffer.append("------------------------------------------\r\n");
		buffer.append("Link: " + this.name + "\r\n");
		buffer.append("Parent: " + this.parent.name + "\r\n");
		buffer.append("Target: " + this.target.name + "\r\n");
		buffer.append("Size: " + this.getSize() + "\r\n");
		buffer.append("Owner: " + this.owner + "\r\n");
		return buffer.toString();
	}
}
