# Generated from E:/UNI/Term6/Compiler/Assignments/pythonProject\MiniJava.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniJavaParser import MiniJavaParser
else:
    from MiniJavaParser import MiniJavaParser

# This class defines a complete listener for a parse tree produced by MiniJavaParser.
class MiniJavaListener(ParseTreeListener):

    # Enter a parse tree produced by MiniJavaParser#program.
    def enterProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#program.
    def exitProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#mainClass.
    def exitMainClass(self, ctx:MiniJavaParser.MainClassContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:MiniJavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx:MiniJavaParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#varDeclaration.
    def enterVarDeclaration(self, ctx:MiniJavaParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#varDeclaration.
    def exitVarDeclaration(self, ctx:MiniJavaParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:MiniJavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:MiniJavaParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#type1.
    def enterType1(self, ctx:MiniJavaParser.Type1Context):
        pass

    # Exit a parse tree produced by MiniJavaParser#type1.
    def exitType1(self, ctx:MiniJavaParser.Type1Context):
        pass


    # Enter a parse tree produced by MiniJavaParser#statement.
    def enterStatement(self, ctx:MiniJavaParser.StatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#statement.
    def exitStatement(self, ctx:MiniJavaParser.StatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#expression.
    def enterExpression(self, ctx:MiniJavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#expression.
    def exitExpression(self, ctx:MiniJavaParser.ExpressionContext):
        pass



del MiniJavaParser