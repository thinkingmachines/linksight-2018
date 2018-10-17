package es.thinkingmachin.linksight.imatch.matcher.tree;

import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;
import java.util.stream.Collectors;

public class TreeExplorer {

    private AddressTreeNode curNode;
    private final TreeReference reference;

    public TreeExplorer(TreeReference reference) {
        this.reference = reference;
        this.curNode = reference.entryPoint;
    }

    public void launchRepl() {
        System.out.println("TreeExplorer REPL");
        boolean exit = false;
        while (!exit) {
            printPrompt();
            Scanner sc = new Scanner(System.in);
            String input = sc.nextLine();
            if (input == null) break;
            String[] terms = input.split("\\s+");
            switch (terms[0]) {
                case "cat":
                    AddressTreeNode c = getNode(terms);
                    if (c == null) continue;
                    System.out.println("Node: "+c.getOrigTerm());
                    System.out.println("PSGC: "+c.psgc);
                    System.out.println("Aliases:");
                    for (String alias: c.aliases) {
                        System.out.println("\t- "+alias);
                    }
                    break;
                case "ls":
                    System.out.println("Children:");
                    curNode.children.stream()
                            .map(child -> "[" + child.psgc +"] "+child.getOrigTerm())
                            .sorted()
                            .forEach(s -> System.out.println("\t- " + s));
                    break;
                case "cd":
                    AddressTreeNode childNode = getNode(terms);
                    if (childNode == null) continue;
                    curNode = childNode;
                    break;
                case "fzy":
                    String word = String.join(" ", Arrays.copyOfRange(terms, 1, terms.length));
                    System.out.println("Clean term: "+curNode.childIndex.namesFuzzyMap.preDict.cleanIndexWord(word));
                    curNode.childIndex.namesFuzzyMap.getFuzzy(word).stream()
                            .sorted(Comparator.comparingDouble(p -> -p.getValue()))
                            .forEach(p -> System.out.println("\t" + p.getKey().getOrigTerm() + ":\t" + p.getValue()));
                    break;
                case "exit":
                    exit = true;
                    break;
                default:
                    System.out.println("Unknown command: " + terms[0]);
                    break;
            }
        }
        System.out.println("Exiting REPL");
    }

    private AddressTreeNode getNode(String[] terms) {
        if (terms.length <= 1) {
            System.out.println("Usage: cd [term]");
            return null;
        }
        String term = String.join(" ", Arrays.copyOfRange(terms, 1, terms.length));
        term = term.trim().toUpperCase();
        if (term.equalsIgnoreCase("..")) {
            AddressTreeNode nextNode = curNode.parent;
            if (nextNode == null) nextNode = reference.root;
            return nextNode;
        } else if (term.equalsIgnoreCase("entrypoint")) {
            return reference.entryPoint;
        }
        AddressTreeNode childNode =  curNode.childIndex.getNodeWithOrigTerm(term);
        if (childNode == null) {
            System.out.println("Cannot find term");
            return null;
        }
        return childNode;
    }

    private void printPrompt() {
        StringBuilder sb = new StringBuilder();
        String ancestry = curNode.getAncestry().stream()
                .map(n -> (n.getOrigTerm() == null) ? "🌲" : n.getOrigTerm())
                .collect(Collectors.joining(" ➤ "));
        sb.append(ancestry);
        sb.append(": ");
        System.out.print(sb);
    }
}
