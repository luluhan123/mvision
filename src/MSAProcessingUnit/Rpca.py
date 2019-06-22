
import math
import numpy.linalg
from numpy.linalg import norm, svd
import numpy as np


class Rpca:
    def __init__(self):
        self.lmbda = 0.01
        self.tol = 1e-7
        self.maxiter = 1000
        self.verbose = True

    def inexact_augmented_lagrange_multiplier(self, X):
        """
        Inexact Augmented Lagrange Multiplier
        """
        Y = X
        self.lmbda = 1 / np.sqrt(X.shape[0])
        norm_two = norm(Y.ravel(), 2)
        norm_inf = norm(Y.ravel(), np.inf) / self.lmbda
        dual_norm = np.max([norm_two, norm_inf])
        Y = Y / dual_norm
        A = np.zeros(Y.shape)
        E = np.zeros(Y.shape)
        dnorm = norm(X, 'fro')
        mu = 1.25 / norm_two
        rho = 1.5
        sv = 10.
        n = Y.shape[0]
        itr = 0
        while True:
            Eraw = X - A + (1 / mu) * Y
            Eupdate = np.maximum(Eraw - self.lmbda / mu, 0) + np.minimum(Eraw + self.lmbda / mu, 0)
            U, S, V = svd(X - Eupdate + (1 / mu) * Y, full_matrices=False)
            svp = (S > 1 / mu).shape[0]
            if svp < sv:
                sv = np.min([svp + 1, n])
            else:
                sv = np.min([svp + round(.05 * n), n])
            Aupdate = np.dot(np.dot(U[:, :svp], np.diag(S[:svp] - 1 / mu)), V[:svp, :])
            A = Aupdate
            E = Eupdate
            Z = X - A - E
            Y = Y + mu * Z
            mu = np.min([mu * rho, mu * 1e7])
            itr += 1
            if ((norm(Z, 'fro') / dnorm) < self.tol) or (itr >= self.maxiter):
                break
        if self.verbose:
            print("Finished at iteration %d" % (itr))
        return A, E

    def robust_pca(self,M):
        """
        Decompose a matrix into low rank and sparse components.
        Computes the RPCA decomposition using Alternating Lagrangian Multipliers.
        Returns L,S the low rank and sparse components respectively
        """
        L = numpy.zeros(M.shape)
        S = numpy.zeros(M.shape)
        Y = numpy.zeros(M.shape)

        mu = (M.shape[0] * M.shape[1]) / (4.0 * self.L1Norm(M))
        lamb = max(M.shape) ** -0.5
        while not self.converged(M, L, S):
            L = self.svd_shrink(M - S + (mu ** -1) * Y, (mu ** -1))
            S = self.shrink(M - L + (mu ** -1) * Y, lamb * (mu ** -1))
            Y = Y + mu * (M - L - S)
        return L, S

    def svd_shrink(self, X, tau):
        """
        Apply the shrinkage operator to the singular values obtained from the SVD of X.
        The parameter tau is used as the scaling parameter to the shrink function.
        Returns the matrix obtained by computing U * shrink(s) * V where
            U are the left singular vectors of X
            V are the right singular vectors of X
            s are the singular values as a diagonal matrix
        """
        U, s, V = numpy.linalg.svd(X, full_matrices=False)
        return numpy.dot(U, numpy.dot(numpy.diag(self.shrink(s, tau)), V))

    def shrink(self, X, tau):
        """
        Apply the shrinkage operator the the elements of X.
        Returns V such that V[i,j] = max(abs(X[i,j]) - tau,0).
        """
        V = numpy.copy(X).reshape(X.size)
        for i in xrange(V.size):
            V[i] = math.copysign(max(abs(V[i]) - tau, 0), V[i])
            if V[i] == -0:
                V[i] = 0
        return V.reshape(X.shape)

    def frobeniusNorm(self,X):
        """
        Evaluate the Frobenius norm of X
        Returns sqrt(sum_i sum_j X[i,j] ^ 2)
        """
        accum = 0
        V = numpy.reshape(X, X.size)
        for i in xrange(V.size):
            accum += abs(V[i] ** 2)
        return math.sqrt(accum)

    def L1Norm(self,X):
        """
        Evaluate the L1 norm of X
        Returns the max over the sum of each column of X
        """
        return max(numpy.sum(X, axis=0))

    def converged(self,M, L, S):
        """
        A simple test of convergence based on accuracy of matrix reconstruction
        from sparse and low rank parts
        """
        error = self.frobeniusNorm(M - L - S) / self.frobeniusNorm(M)
        return error <= 10e-6



