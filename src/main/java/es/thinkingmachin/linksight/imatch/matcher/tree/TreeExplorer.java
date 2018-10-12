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
        this.curNode = reference.root;
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
                case "ls":
                    System.out.println("Children:");
                    curNode.getChildTerms().stream()
                            .sorted()
                            .forEach(s -> System.out.println("\t- " + s));
                    break;
                case "cd":
                    if (terms.length <= 1) {
                        System.out.println("Usage: cd [term]");
                        continue;
                    }
                    String term = String.join(" ", Arrays.copyOfRange(terms, 1, terms.length));
                    term = term.trim().toUpperCase();
                    if (term.equals("..")) {
                        curNode = curNode.parent;
                        if (curNode == null) curNode = reference.root;
                        continue;
                    }
                    AddressTreeNode childNode = curNode.getChildWithOrigTerm(term);
                    if (childNode == null) {
                        System.out.println("Cannot find term: " + term);
                        continue;
                    }
                    curNode = childNode;
                    break;
                case "fzy":
                    String word = String.join(" ", Arrays.copyOfRange(terms, 1, terms.length));
                    curNode.fuzzyStringMap.getFuzzy(word).stream()
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
